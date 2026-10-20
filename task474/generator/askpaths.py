"""The asks computed from the grants data system's rows as the pack ships them, under any combination of the four
handlings the extract needs: the resent upload dropped, FY2026 kept by service date, Corbin's earlier client numbers
converted, and each client's town on the service date taken from the profile audit trail; energy assistance once per
household payment. The golden takes all of them; the careful path reads the extract as it stands."""
import datetime as dt

import asks as A
import world as W

FY0, FY1 = A.FY_START, A.FY_END


def figures(ext, aud, conv, balances, dedup=True, fy=True, convert=True, history=True, per_household=True):
    code2agency = {v: k for k, v in A.CODE.items()}
    region = {t["name"]: t["region"] for t in W.TOWNS}
    rows = [tuple(str(v) for v in r) for r in ext]
    if dedup:
        seen, out = set(), []
        for r in rows:
            if r not in seen:
                seen.add(r)
                out.append(r)
        rows = out
    if fy:
        rows = [r for r in rows if FY0 <= dt.date.fromisoformat(r[4]) <= FY1]
    o2n = {str(a): str(b) for a, b, _ in conv}
    pid = (lambda c: o2n.get(c, c)) if convert else (lambda c: c)
    hist = {}
    if history:
        for a in aud:
            if a[2] == "town":
                hist.setdefault(pid(str(a[1])), []).append((dt.date.fromisoformat(a[5]), a[3], a[4]))
        for v in hist.values():
            v.sort()

    def town_at(r):
        h = hist.get(pid(r[1]))
        if not h:
            return r[6]
        d = dt.date.fromisoformat(r[4])
        cur = h[0][1]
        for eff, old, new in h:
            if eff <= d:
                cur = new
        return cur
    n = {}
    for r in rows:
        n.setdefault((code2agency[r[0]], region[town_at(r)]), set()).add(pid(r[1]))
    counts = {k: len(v) for k, v in n.items()}
    carry = {g: 0.0 for g in W.REGION_NAMES}
    people = {g: 0 for g in W.REGION_NAMES}
    for c in W.COUNTY_NAMES:
        tot = sum(v for (a, g), v in counts.items() if a == c)
        for (a, g), v in counts.items():
            if a == c:
                carry[g] += balances[c]["unspent"] * v / tot
                people[g] += v
    energy = {g: 0.0 for g in W.REGION_NAMES}
    seen = set()
    for r in rows:
        if r[3] != "EA":
            continue
        if per_household:
            k = (r[2], r[4], r[7])
            if k in seen:
                continue
            seen.add(k)
        energy[region[town_at(r)]] += float(r[7])
    return dict(carry=carry, people=people, energy=energy, counts=counts)


STOPS = {
    "golden": {},
    "careful": dict(convert=False, history=False, per_household=False),
    "history only": dict(convert=False, per_household=False),
    "conversion only": dict(history=False, per_household=False),
    "one payment per household only": dict(convert=False, history=False),
    "history and one payment per household": dict(convert=False),
    "conversion and one payment per household": dict(history=False),
    "every row the extract holds": dict(fy=False),
}
