"""The analysis on the shipped pack: each region's vehicle-years and accident claims over the 2024 and 2025 accident
years, the ladder (the reported frequency, the Step Protection lift on steps 6 to 9 and on every step, and the
size-based recovery of the claims the old wording kept out of the record), band C, and the two asks (the 2025
windscreen and theft rates). Every figure is computed from the files in target/."""
import datetime as dt

import common as K
import pack as PK

T_GOLDEN = 2500.0            # the size above which no policyholder's own payment reaches (the golden's threshold)
T_GRID = (1500.0, 2000.0, 2500.0, 3000.0)


def accident_claims(P, years=K.ACC_YEARS, when="loss", keep=None, skipped=None):
    """Accident claims with an amount paid or reserved above nil, dated in the accident years, each with its
    policy year, region on the accident date, step and protection at inception. (when and keep serve the checks'
    readings; a claim no policy year covers is listed in skipped.)"""
    out = []
    for c in P["claims"]:
        if c["type"] != "ACC" or c["incurred"] <= 0 or c[when].year not in years:
            continue
        if keep is not None and not keep(c):
            continue
        t = PK.term_for(P, c["ref"], c["loss"])
        if t is None:
            if skipped is not None:
                skipped.append(c["no"])
            continue
        d, _ = PK.state_on(t, c["loss"])
        out.append(dict(c, region=P["rmap"].region(d, c["loss"]), step=t["step"], prot=t["prot"],
                        full=t["step"] == 0 or t["prot"]))
    return out


def top3(v):
    o = sorted(K.CODES, key=lambda c: -v[c])
    return dict(band=o[:3], below=o[3], order=o, margin=v[o[2]] / v[o[3]] - 1.0)


def reported(E, A):
    n = {c: 0 for c in K.CODES}
    for a in A:
        n[a["region"]] += 1
    return n, {c: 100.0 * n[c] / E[c] for c in K.CODES}


def lift(P, A, steps=K.PILOT_STEPS):
    """The analyst's lift: the Step Protection holders' claim frequency over other policyholders' on steps 6 to 9,
    applied to the unprotected policies on the given steps."""
    Es = PK.exposure(P, K.ACC_YEARS, by=("region", "step", "prot"))
    num = {True: 0, False: 0}
    den = {True: 0.0, False: 0.0}
    for (r, s, pr), v in Es.items():
        if s in K.PILOT_STEPS:
            den[pr] += v
    for a in A:
        if a["step"] in K.PILOT_STEPS:
            num[a["prot"]] += 1
    u = (num[True] / den[True]) / (num[False] / den[False])
    E = {c: sum(v for (r, s, pr), v in Es.items() if r == c) for c in K.CODES}
    n = {c: 0.0 for c in K.CODES}
    for a in A:
        n[a["region"]] += u if (a["step"] in steps and not a["prot"]) else 1.0
    return u, {c: 100.0 * n[c] / E[c] for c in K.CODES}


def share_above(A, T, source="both"):
    pick = {"both": lambda a: a["full"], "step0": lambda a: a["step"] == 0, "prot": lambda a: a["prot"]}[source]
    base = [a["incurred"] for a in A if pick(a)]
    return sum(1 for x in base if x > T) / len(base), len(base)


def recovered(E, A, T=T_GOLDEN, source="both"):
    """Claims above T are complete on every step; each region's claims above T over the share of claims that large
    among the policies a claim costs nothing (step 0 and Step Protection) recover the claims made under protection."""
    S, nbase = share_above(A, T, source)
    n = {c: 0 for c in K.CODES}
    for a in A:
        if a["incurred"] > T:
            n[a["region"]] += 1
    return S, {c: n[c] / S for c in K.CODES}, {c: 100.0 * n[c] / S / E[c] for c in K.CODES}


def recovered_insured(E, A, T=T_GOLDEN):
    """The same recovery applied only to the claims of policies that pay for a claim with their steps (steps 1 to 9
    without Step Protection), the full reporters' claims taken as made."""
    S, _ = share_above(A, T)
    n = {c: 0.0 for c in K.CODES}
    for a in A:
        if a["full"]:
            n[a["region"]] += 1
        elif a["incurred"] > T:
            n[a["region"]] += 1.0 / S
    return {c: 100.0 * n[c] / E[c] for c in K.CODES}


def size_profile(A, edges=(0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000, 4000, 6000, 1e12)):
    """Claims by size band for the full reporters and for the other policies (the comparison that shows the cut)."""
    rows = []
    full = [a["incurred"] for a in A if a["full"]]
    rest = [a["incurred"] for a in A if not a["full"]]
    for lo, hi in zip(edges, edges[1:]):
        rows.append((lo, hi, sum(lo < x <= hi for x in full), sum(lo < x <= hi for x in rest)))
    return rows


# ------------------------------------------------------------------------------------------------- the asks
def partner_jobs(P):
    """The partner's jobs billed to the Society: a job's lines are one claim, at their amount with VAT."""
    jobs = {}
    for g in P["glass"]:
        if g["billed"] != K.SHORT:
            continue
        j = jobs.setdefault(g["job"], dict(job=g["job"], booked=g["booked"], ref=g["ref"], gross=0.0, net=0.0))
        j["gross"] += g["net"] + g["vat"]
        j["net"] += g["net"]
    return jobs


def feed_matches(P, jobs):
    """The platform's windscreen claims that are the partner's jobs again: same policy number, registered on the day
    the partner booked the job, at the job's amount before VAT. Returns {claim number: job reference}."""
    index = {}
    for j in jobs.values():
        index.setdefault((j["ref"], j["booked"], round(j["net"], 2)), []).append(j["job"])
    out = {}
    for c in P["claims"]:
        if c["type"] != "WSC" or c["sys"] != "P":
            continue
        hit = index.get((c["ref"], c["notified"], round(c["incurred"], 2)))
        if hit:
            out[c["no"]] = hit
    return out


def windscreen(P, E25c):
    """Ask A: each region's 2025 windscreen claims per 100 comprehensive vehicle-years and their average cost
    including VAT: the partner's jobs billed to the Society, and the claims of repairers the policyholder chose (the
    claims that are not the partner's jobs registered again on the platform)."""
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    jobs = partner_jobs(P)
    feed = feed_matches(P, jobs)
    for j in jobs.values():
        if j["booked"].year != 2025:
            continue
        t = PK.term_for(P, j["ref"], j["booked"])
        d, cv = PK.state_on(t, j["booked"])
        r = P["rmap"].region(d, j["booked"])
        n[r] += 1
        cost[r] += j["gross"]
    own = 0
    for c in P["claims"]:
        if c["type"] != "WSC" or c["no"] in feed or c["notified"].year != 2025 or c["incurred"] <= 0:
            continue
        t = PK.term_for(P, c["ref"], c["notified"])
        d, cv = PK.state_on(t, c["notified"])
        r = P["rmap"].region(d, c["notified"])
        n[r] += 1
        cost[r] += c["incurred"]
        own += 1
    freq = {c: 100.0 * n[c] / E25c[c] for c in K.CODES}
    avg = {c: cost[c] / n[c] for c in K.CODES}
    return dict(n=n, cost=cost, freq=freq, avg=avg, own=own, feed=len(feed),
                jobs=len([j for j in jobs.values() if j["booked"].year == 2025]))


def thefts(P, E25):
    """Ask B: each region's 2025 thefts per 100 vehicle-years and their average cost net of salvage: a theft's claims
    share its police crime reference (written with separators on the legacy system), it is dated by its earliest
    claim's loss date, and its cost is every claim's incurred less the salvage agent's net proceeds."""
    groups = {}
    for c in P["claims"]:
        if c["type"] != "THF":
            continue
        groups.setdefault(c["police"], []).append(c)
    net = {}
    for s in P["salvage"]:
        net[s["claim"]] = net.get(s["claim"], 0.0) + s["net"]
    n = {c: 0 for c in K.CODES}
    cost = {c: 0.0 for c in K.CODES}
    for ref, cs in groups.items():
        first = min(cs, key=lambda c: (c["loss"], c["notified"], c["no"]))
        if first["loss"].year != 2025:
            continue
        inc = sum(c["incurred"] for c in cs)
        if inc <= 0:
            continue
        t = PK.term_for(P, first["ref"], first["loss"])
        d, _ = PK.state_on(t, first["loss"])
        r = P["rmap"].region(d, first["loss"])
        n[r] += 1
        cost[r] += inc - sum(net.get(c["no"], 0.0) for c in cs)
    freq = {c: 100.0 * n[c] / E25[c] for c in K.CODES}
    avg = {c: cost[c] / n[c] for c in K.CODES}
    return dict(n=n, cost=cost, freq=freq, avg=avg)


def run(target):
    P = PK.load(target)
    E = {k[0]: v for k, v in PK.exposure(P, K.ACC_YEARS).items()}
    A = accident_claims(P)
    n0, R0 = reported(E, A)
    u, R1 = lift(P, A)
    _, R1b = lift(P, A, steps=range(1, 10))
    S, N2, R2 = recovered(E, A)
    grid = {}
    for T in T_GRID:
        for src in ("both", "step0", "prot"):
            grid[(T, src)] = recovered(E, A, T, src)[2]
    R2i = recovered_insured(E, A)
    E25 = {k[0]: v for k, v in PK.exposure(P, (2025,)).items()}
    E25c = {k[0]: v for k, v in PK.exposure(P, (2025,), cover="COMP").items()}
    return dict(P=P, E=E, A=A, n0=n0, R0=R0, u=u, R1=R1, R1b=R1b, S=S, N2=N2, R2=R2, grid=grid, R2i=R2i,
                profile=size_profile(A), E25=E25, E25c=E25c, glass=windscreen(P, E25c), theft=thefts(P, E25))


if __name__ == "__main__":
    import os
    import sys
    import time
    t0 = time.time()
    res = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "target"))
    print("%.0fs" % (time.time() - t0))
    for nm in ("R0", "R1", "R1b", "R2", "R2i"):
        v = res[nm]
        t = top3(v)
        print(nm, t["band"], "below", t["below"], "margin %.3f" % t["margin"],
              " ".join("%s %.2f" % (c, v[c]) for c in K.CODES))
    print("u %.3f S %.3f" % (res["u"], res["S"]))
    for k, v in sorted(res["grid"].items()):
        t = top3(v)
        print(k, sorted(t["band"]), t["below"], "%.3f" % t["margin"])
    for row in res["profile"]:
        print(row)
    g, th = res["glass"], res["theft"]
    for c in K.CODES:
        print(c, "E %.0f E25 %.0f E25c %.0f" % (res["E"][c], res["E25"][c], res["E25c"][c]),
              "glass %d %.2f %.2f" % (g["n"][c], g["freq"][c], g["avg"][c]),
              "theft %d %.3f %.2f" % (th["n"][c], th["freq"][c], th["avg"][c]))
