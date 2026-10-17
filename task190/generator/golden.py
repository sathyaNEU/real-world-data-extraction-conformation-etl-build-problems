"""The figure the committee paper carries, and every rung below it."""
import mus
import world as W


def compute(lines, hits):
    rec = {c: sum(x[1] for x in lines if x[0] == c) for c in W.PROG_CODES}
    tested, cert, prop = mus.split(lines, hits)
    certv = {c: sum(x[1] for x in lines if x[0] == c and x[1] >= W.INTERVAL)
             for c in W.PROG_CODES}
    pp = mus.projection(lines, hits, by_programme=True)
    ev = mus.evaluation(lines, hits)
    per = {c: mus.r_grain(pp[c]) for c in W.PROG_CODES}
    total = sum(per.values())
    largest = max(W.PROG_CODES, key=lambda c: (per[c], pp[c]))
    return dict(
        recorded=rec, recorded_total=sum(rec.values()),
        certain_share={c: round(100.0 * certv[c] / rec[c], 1) for c in W.PROG_CODES},
        per=per, per_raw=pp, total=total, total_raw=ev["pm"],
        bp=ev["bp"], ia=ev["ia"], uml=ev["uml"], crude=ev["crude"], n_taint=ev["n_taint"],
        found=mus.found(lines, hits), ratio=mus.recorded_ratio(lines, hits),
        stratum=mus.stratum_ratio(lines, hits),
        tested_lines=len(tested), tested_value=sum(x[1] for x in tested),
        cert_lines=len(cert), cert_value=sum(x[1] for x in cert),
        largest=largest, referred=ev["uml"] > W.TOLERABLE,
        lattice=mus.lattice(lines, hits, W.INTERVAL),
        routes=mus.routes(lines, hits))


def rungs(g):
    return [("the misstatement the testing found", g["found"]),
            ("the errors found scaled on recorded value", g["ratio"]),
            ("certainty lines at their own error, the rest on their stratum", g["stratum"]),
            ("each tainting at the recovered interval", g["total_raw"])]
