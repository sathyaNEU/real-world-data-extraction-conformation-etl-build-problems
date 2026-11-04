"""The world, its golden and every route, built from one seed; and the seed search that keeps the first world in
which every graded figure is robust and every route files its own wrong answer.

Pure integer and rational arithmetic; nothing here depends on a numerical library or a CPU path."""
from fractions import Fraction
from rng import Rng
import sim
import world
import routes
from sim import T0, T1, T_SUSP, SECTIONS

SEED_BASE = 4880
SEED_TRIES = 120
RK_TRIES = 400
CERTS = {   # batch, tank, density at 15 C (tenths of kg/m3), conductivity (pS/m)
    "aged": ("J-26-1102", "Tank 4", 7990, 151),
    "old": ("J-26-1171", "Tank 2", 8036, 236),
    "batch": ("J-26-1187", "Tank 3", 7954, 88),
    "new": ("J-26-1179", "Tank 1", 8013, 312),
}
BATCH_TANKS = ("RF-23", "RF-24", "T-31", "T-35")
CRACKER_COUPLINGS = [(-10 ** 9, trac, trl) for trac, trl in world.REGISTER_PAIRING.items()]


def rnd(v, unit):
    """Half up to a multiple of unit, for integers or Fractions."""
    v = Fraction(v)
    return int((v / unit + Fraction(1, 2)) // 1) * unit


def edge_margin(v, unit):
    """Distance from v to the nearest edge of the cell it rounds into."""
    v = Fraction(v)
    return Fraction(unit, 2) - abs(v - rnd(v, unit))


def density_gap(a, b):
    return abs(CERTS[a][2] - CERTS[b][2])


def refueller_view(W, **kw):
    d, lb, tanks, ext = world.simulate_rack_and_tanks(W["loads"], W["rups"], W["opening"], transfers=W["xfers"], **kw)
    by_air, by_air_rows = {}, {}
    n_up = 0
    for u in W["rups"]:
        b = d.get(u.uid, 0)
        if b > 0:
            by_air[u.airline] = by_air.get(u.airline, Fraction(0)) + b
            by_air_rows[u.airline] = by_air_rows.get(u.airline, 0) + rnd(b, 10)
            n_up += 1
    held = {k: v[0] for k, v in tanks.items()}
    return {"delivered": d, "load_batch": lb, "tanks": tanks, "held": held, "by_air": by_air, "n_up": n_up,
            "by_air_rows": by_air_rows,
            "extremes": ext, "set": sorted(k for k, v in held.items() if v > 0)}


def build(seed, rk=None):
    """The hydrant world from the seed; with rk, the refueller day from its own fork (see add_refuellers)."""
    rng = Rng(seed)
    fleet = sim.Fleet(rng)
    ups = world.hydrant_schedule(rng, fleet)
    for i, u in enumerate(ups):
        u.uid = i
    drains, checks = world.drains_and_checks(ups, rng)
    for i, d in enumerate(drains):
        d.uid = 10000 + i
    hyd = ups + drains
    pcs = world.product_change_checks(ups, drains)
    samples = checks + pcs
    W = {"seed": seed, "rng": rng, "fleet": fleet, "ups": ups, "drains": drains, "hyd": hyd, "checks": checks,
         "pcs": pcs, "samples": samples, "flights0": dict(fleet.flights)}
    G = routes.golden(hyd, samples)
    W["gold"] = G
    W["standing"] = G["standing"]
    W["took"] = {u: v for u, v in G["took"].items() if u < 10000}
    W["drained"] = [s for s in SECTIONS if G["standing"][s] > 0]
    if rk is not None:
        add_refuellers(W, rk)
    return W


def add_refuellers(W, rk):
    """The refueller day from fork rk of the seed (fork 0 is 'refuellers'), the fleet's flight numbers reset to the
    hydrant day's so every attempt draws from the same state."""
    W["fleet"].flights = dict(W["flights0"])
    tag = "refuellers" if rk == 0 else "refuellers-%d" % rk
    rups, loads, xfers, opening = world.refueller_schedule(W["rng"], W["fleet"], tag)
    for i, u in enumerate(rups):
        u.uid = 5000 + i
    W.update({"rk": rk, "rups": rups, "loads": loads, "xfers": xfers, "opening": opening})
    W["ref"] = refueller_view(W)
    return W


def profile(ups, where):
    """Each draw taken as one minute's flow at its start, middle or end: the readings of a ticket that ignore its
    steady rate between the start and the end the pump station's minute flows show."""
    import copy
    out = []
    for u in ups:
        v = copy.copy(u)
        v.start = {"start": u.start, "end": u.end - sim.M, "mid": u.start + (u.dur // 2) // sim.M * sim.M}[where]
        v.dur = sim.M
        out.append(v)
    return out


def variants(W, profiles=True):
    hyd, samples = W["hyd"], W["samples"]
    out = {"net": routes.golden(hyd, samples, litres="net"),
           "no_flush": routes.golden(hyd, samples, kinds=("hydrant",))}
    for d0 in (-90, 90):
        for d1 in (-90, 90):
            out["edges%+d%+d" % (d0, d1)] = routes.golden(hyd, samples, edges=(T0 + d0, T1 + d1))
    if profiles:
        for where in ("start", "mid", "end"):
            out["at_" + where] = routes.golden(profile(hyd, where), samples)
    return out


def batch15(u, batch, litres="gross"):
    """Litres of the batch at 15 C in an uplift: its litres at 15 C times the batch's share of what it drew."""
    if litres == "net":
        return batch
    return (2 * batch * u.net + u.gross) // (2 * u.gross)


def batch15_total(W, G, litres="gross"):
    by = {u.uid: u for u in W["ups"]}
    return sum(batch15(by[k], v, litres) for k, v in G["took"].items() if k < 10000)


def contradictions(labels, gold_labels, samples, floor=20):
    """Samples a route mispredicts by at least `floor` tenths of kg/m3 of density at 15 C."""
    out = []
    for s in samples:
        k = (s["time"], s["pit"])
        if density_gap(labels[k], gold_labels[k]) >= floor:
            out.append(k)
    return out


def branch_statistics(W):
    """Each branch's draws after 06:00 and after 15:40, its line fill and its draws per line fill after 15:40."""
    hyd = W["hyd"]
    out = {}
    for sec in sim.BRANCHES:
        d0 = sum(u.cum(T_SUSP) - u.cum(T0) for u in hyd if sim.PIT_SECTION[u.pit] == sec)
        d1 = sum(u.cum(T_SUSP) - u.cum(T1) for u in hyd if sim.PIT_SECTION[u.pit] == sec)
        lf = sim.section_fill(sec)
        out[sec] = {"drew_after_0600": d0, "drew_after_1540": d1, "line_fill": lf, "turnovers_after_1540": Fraction(d1, lf)}
    return out


def interval_sorts(W):
    """The statistics on which the golden set is a contiguous run of the six branches sorted (the Shock test)."""
    st = branch_statistics(W)
    bad = []
    for key in ("drew_after_0600", "drew_after_1540", "line_fill", "turnovers_after_1540"):
        order = sorted(sim.BRANCHES, key=lambda s: (st[s][key], s))
        pos = sorted(order.index(s) for s in W["drained"])
        if pos == list(range(pos[0], pos[0] + len(pos))):
            bad.append(key)
    return bad


def screen(W, full=True):
    """Every condition the world must meet; returns (ok, report)."""
    rep, ok = {}, True
    G = W["gold"]
    took = set(W["took"])
    rep["drained"] = W["drained"]
    ok &= W["drained"] == ["B", "E", "F"]
    if ok:
        rep["interval_sorts"] = interval_sorts(W)
        ok &= not rep["interval_sorts"]
    small = sorted(W["took"].values())[:3]
    rep["smallest_exposures"] = small
    ok &= small[0] >= 250
    if not ok and not full:
        return ok, rep
    V = variants(W)
    rep["set_diffs"] = {k: len({u for u in g["took"] if u < 10000} ^ took) for k, g in V.items()}
    ok &= all(v == 0 for k, v in rep["set_diffs"].items() if not k.startswith("at_"))
    tot = {"gold": batch15_total(W, G)}
    for k, g in V.items():
        if not k.startswith("at_"):
            tot[k] = batch15_total(W, g, litres="net" if k == "net" else "gross")
    rep["batch15_total"] = tot["gold"]
    cells = {rnd(v, 1000) for v in tot.values()}
    rep["batch15_margin"] = int(min(edge_margin(v, 1000) for v in tot.values())) if len(cells) == 1 else -1
    rep["labels_stable"] = {k: sum(1 for x in G["labels"] if g["labels"][x] != G["labels"][x]) for k, g in V.items()}
    ok &= all(v == 0 for k, v in rep["labels_stable"].items() if not k.startswith("at_"))
    margins = {}
    rep["standing_profiles"] = {k: [g["standing"][s] for s in W["drained"]] for k, g in V.items() if k.startswith("at_")}
    for s in W["drained"]:
        vals = [G["standing"][s]] + [g["standing"][s] for k, g in V.items() if not k.startswith("at_")]
        cells = {rnd(v, 100) for v in vals}
        margins[s] = int(min(edge_margin(v, 100) for v in vals)) if len(cells) == 1 else -1
    rep["standing_margins"] = margins
    ok &= all(m >= 15 for m in margins.values())
    # every route files its own wrong answer and is refuted by the shipped samples
    rep["routes"] = {}
    for name, fn in routes.ROUTES.items():
        R = fn(W["hyd"], W["samples"])
        rt = {u for u in R["took"] if u < 10000}
        drained = [s for s in SECTIONS if R["standing"][s] > 0]
        con = contradictions(R["labels"], G["labels"], W["samples"])
        rep["routes"][name] = {"extra": len(rt - took), "missed": len(took - rt), "drained": drained,
                               "contradicted": len(con)}
        ok &= len(rt ^ took) >= 3 and drained != W["drained"] and len(con) >= 4
    return ok, rep


def screen_refuellers(W):
    """The refueller day: the truth, the cracker's view (fleet list pairing, no transfer) and the mirror's (no
    header either); returns (ok, report)."""
    rep, ok = {}, True
    ref = W["ref"]
    cr = refueller_view(W, couplings=CRACKER_COUPLINGS, with_transfers=False)
    mi = refueller_view(W, couplings=CRACKER_COUPLINGS, with_transfers=False, header=0)
    W["cracker_ref"], W["mirror_ref"] = cr, mi
    rep["ref_set"] = ref["set"]
    ok &= ref["set"] == sorted(BATCH_TANKS)
    for nm, view in (("cracker", cr), ("mirror", mi)):
        for k, (lo, hi) in view["extremes"].items():
            ok &= lo >= 0 and hi <= world.TANKS[k][1]
    figs = [ref["held"][k] for k in BATCH_TANKS] + list(ref["by_air"].values())
    rep["ref_min_margin"] = float(min(edge_margin(v, 10) for v in figs))
    ok &= rep["ref_min_margin"] >= 1
    ok &= all(rnd(ref["by_air"][a], 10) == rnd(ref["by_air_rows"][a], 10) for a in ref["by_air"])
    rep["ref_round_hundreds"] = [x for x in (rnd(v, 10) for v in figs) if x % 100 == 0]
    ok &= not rep["ref_round_hundreds"]
    sep = {}
    for nm, view in (("cracker", cr), ("mirror", mi)):
        d = [abs(rnd(ref["held"][k], 10) - rnd(view["held"].get(k, 0), 10)) for k in BATCH_TANKS]
        d += [abs(rnd(ref["by_air"].get(a, 0), 10) - rnd(view["by_air"].get(a, 0), 10))
              for a in sorted(set(ref["by_air"]) | set(view["by_air"]))]
        d.append(10 * abs(ref["n_up"] - view["n_up"]))
        sep[nm] = min(d)
    rep["ref_separation"] = sep
    ok &= all(v >= 20 for v in sep.values())
    ok &= len(ref["by_air"]) == 6
    return ok, rep


def search(verbose=False):
    for k in range(SEED_TRIES):
        seed = SEED_BASE + k
        W = build(seed)
        ok, rep = screen(W, full=False)
        if ok:
            ok, rep = screen(W)
        if verbose:
            print(seed, ok, rep)
        if not ok:
            continue
        for rk in range(RK_TRIES):
            add_refuellers(W, rk)
            rok, rrep = screen_refuellers(W)
            if rok:
                W["screen"] = rep
                W["screen_ref"] = rrep
                if verbose:
                    print("  refuellers fork", rk, rrep)
                return W
    raise SystemExit("no seed in %d tries meets every condition" % SEED_TRIES)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            W = build(int(s), 0)
            print(s, screen(W), screen_refuellers(W))
    else:
        W = search(verbose=True)
        print("chosen", W["seed"])
