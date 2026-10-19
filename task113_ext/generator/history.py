"""What each security was called, traded as and classified as on every day: the security master's spells, built
from the listing, renamings (a new descriptor, or a full rebrand with a new name, ticker and CUSIP issuer), ticker
changes (two of them taking a ticker an earlier, delisted company had used), exchange transfers, the classification
review of March 2023, and the new CUSIP issue number a reverse split brings."""
import datetime as dt

import universe as U
import world as W


def build(secs, paths):
    rng = U.rng_for(6)
    roots = U._roots(U.rng_for(1))
    spare = roots[len(secs):len(secs) + 40]
    taken_names = {s["root"] for s in secs}
    hist = {}
    used = {}            # ticker -> list of (from_i, to_i)

    def free(tk, a, b):
        return all(b < u0 or a > u1 for u0, u1 in used.get(tk, []))

    def claim(tk, a, b):
        used.setdefault(tk, []).append((a, b))

    for s in sorted(secs, key=lambda s: s["first"]):
        a = s["first"]
        b = s["last"] if s["last"] is not None else U.T - 1
        cur = dict(ticker=s["ticker"], name=s["name"], exch=s["exch"], issuer=s["issuer"], issue="10",
                   sector=s["sector"], desc=s["desc"], root=s["root"], legal=s["legal"])
        spells = [(a, dict(cur))]
        for kind, day, arg in s["events"]:
            if kind == "rename":
                if rng.random() < 0.5:
                    root = spare.pop(0)
                    while root in taken_names:
                        root = spare.pop(0)
                    taken_names.add(root)
                    cur["root"] = root
                    cur["issuer"] = U.make_cusip(rng, set())
                    cur["ticker"] = U._ticker(root, cur["exch"], set(used), rng)
                descs = W.SECTORS[cur["sector"]][2]
                before = cur["name"]
                while cur["name"] == before:
                    new_desc = [d for d in descs if d != cur["desc"]]
                    cur["desc"] = new_desc[int(rng.integers(len(new_desc)))] if rng.random() < 0.7 else ""
                    cur["legal"] = U._legal(rng, cur["desc"])
                    cur["name"] = U.issuer_name(cur["root"], cur["desc"], cur["legal"])
            elif kind == "ticker_change":
                cur["ticker"] = U._ticker(cur["root"] + cur["desc"][:3], cur["exch"], set(used) | {cur["ticker"]}, rng)
            elif kind == "exchange_transfer":
                cur["exch"] = arg
            elif kind == "reclassify":
                cur["sector"] = arg
                descs = W.SECTORS[arg][2]
                cur["desc_class"] = descs[int(rng.integers(len(descs)))]
            elif kind == "reverse_split":
                cur["issue"] = str(int(cur["issue"]) + 10)
            else:
                continue
            spells.append((day, dict(cur)))
        # every ticker this security uses must be free over its spell
        fixed = []
        for idx, (d0, sp) in enumerate(spells):
            d1 = spells[idx + 1][0] - 1 if idx + 1 < len(spells) else b
            tk = sp["ticker"]
            while not free(tk, d0, d1):
                tk = U._ticker(sp["root"] + "X", sp["exch"], set(used), rng)
            sp["ticker"] = tk
            claim(tk, d0, d1)
            fixed.append((d0, d1, sp))
        hist[s["k"]] = fixed
    _recycle(secs, hist, used, rng)
    for s in secs:
        for d0, d1, sp in hist[s["k"]]:
            sp["cusip"] = U.full_cusip(sp["issuer"], sp["issue"])
    return hist


def _recycle(secs, hist, used, rng):
    """Two later listings take a ticker that a company delisted at least a year earlier had traded under."""
    gone = [s for s in secs if s["last"] is not None]
    later = [s for s in secs if s["kind"] == "ipo"]
    done = 0
    for s in sorted(later, key=lambda s: -s["first"]):
        if done == 2:
            break
        for g in sorted(gone, key=lambda g: g["last"]):
            if g["last"] + 260 < s["first"]:
                old_tk = hist[g["k"]][-1][2]["ticker"]
                d0, d1, sp = hist[s["k"]][0]
                end = hist[s["k"]][-1][1]
                if all(e < d0 or st > end for st, e in used.get(old_tk, []) if (st, e) != (g["first"], g["last"])
                       ) and len(old_tk) <= (4 if sp["exch"] == "Q" else 3):
                    if any(h[2]["ticker"] == old_tk for k2, hh in hist.items() for h in hh if k2 != g["k"]):
                        continue
                    for idx, (a, b, spx) in enumerate(hist[s["k"]]):
                        if spx["ticker"] == sp["ticker"]:
                            spx["ticker"] = old_tk
                    used.setdefault(old_tk, []).append((d0, end))
                    s["recycled_from"] = g["k"]
                    gone.remove(g)
                    done += 1
                    break


def on(hist, k, i):
    """The spell of security k in force on day index i."""
    for d0, d1, sp in hist[k]:
        if d0 <= i <= d1:
            return sp
    return None
