"""The golden, computed from the pack alone (bundle.py): every 2021 live tree's 2026 fate with the trees the
contract crews tallied again under new tags linked back by stem map, species and size, each stand's 2021 to 2026
loss of 2021 live basal area against the policy's 15 per cent, its 2026 live basal area and net Scribner volume per
acre; then the two deliverables and generator/figures.json. Route arguments let checks.py and ceiling.py run the
easy paths through the same code."""
import csv
import io
import json
import math
import os

import bundle as B
import world as W

TOL_FT = 3.0
GROW = (-0.4, 3.2)


def ba(d):
    return W.BA_K * d * d


def r1(v):
    return math.floor(v * 10 + 0.5) / 10


def r10(v):
    return int(math.floor(v / 10 + 0.5) * 10)


def xy(az, dist):
    return dist * math.sin(math.radians(az)), dist * math.cos(math.radians(az))


def resolve(d, tol=TOL_FT, grow=GROW, centric="N", species_check=True):
    """Classify the 2026 records. centric N: every added (N) record is compared with the 2021 live trees on its plot;
    centric M: only trees not found (M) are looked for among the added records (the added records standing on a tree
    that was found are never examined)."""
    alpha = {k: v["company_code"] for k, v in d["spp"].items()}
    on_plot = {}
    for t in d["live21"].values():
        on_plot.setdefault(t["plot"], []).append(t)
    rec = {}
    added = []
    for r in d["t26"]:
        if r["status"] == "N":
            added.append(r)
        else:
            rec[r["tag"]] = r
    retag, dup, new, odd, amb = {}, set(), [], [], []

    def ok(t, r):
        if r["az"] is None or t["az"] is None:
            return False
        x0, y0 = xy(t["az"], t["dist"])
        x1, y1 = xy(r["az"], r["dist"])
        if (x0 - x1) ** 2 + (y0 - y1) ** 2 > tol * tol:
            return False
        if species_check and alpha[r["fia"]] != t["spp"]:
            return False
        return grow[0] <= r["dbh"] - t["dbh21"] <= grow[1]

    if centric == "N":
        for r in added:
            c = [t for t in on_plot.get(r["plot"], []) if ok(t, r)]
            if len(c) > 1:
                amb.append((r["plot"], r["tag"]))
                continue
            if not c:
                new.append(r)
                continue
            s = rec[c[0]["tag"]]["status"]
            if s == "M":
                if c[0]["tag"] in retag:
                    amb.append((r["plot"], r["tag"]))
                retag[c[0]["tag"]] = r
            elif s == "L":
                dup.add((r["plot"], r["tag"]))
            else:
                odd.append((r["plot"], r["tag"], s))
    else:
        used = set()
        for t in d["live21"].values():
            if rec[t["tag"]]["status"] != "M":
                continue
            c = [r for r in added if r["plot"] == t["plot"] and ok(t, r)]
            if len(c) == 1 and (c[0]["plot"], c[0]["tag"]) not in used:
                retag[t["tag"]] = c[0]
                used.add((c[0]["plot"], c[0]["tag"]))
            elif len(c) > 1:
                amb.append((t["plot"], t["tag"]))
        new = [r for r in added if (r["plot"], r["tag"]) not in used]
    return dict(retag=retag, dup=dup, new=new, odd=odd, amb=amb, rec=rec, added=added)


def fates(d, res, route="LINK"):
    """Each 2021 live tree's 2026 fate. LINK: the golden. TAG: the tag join (no record under the 2021 tag reads as
    lost). EXCL: trees not found are set aside (out of both sides of the share)."""
    out = {}
    for tag, t in d["live21"].items():
        r = res["rec"][tag]
        s = r["status"]
        if s == "L":
            f = ("live", tag, r["dbh"])
        elif s == "D":
            f = ("dead", None, None)
        elif s == "C":
            f = ("cut", None, None)
        elif s == "M":
            if route == "LINK" and tag in res["retag"]:
                n = res["retag"][tag]
                f = ("live", n["tag"], n["dbh"])
            elif route == "EXCL":
                f = ("unknown", None, None)
            else:
                f = ("missing", None, None)
        else:
            raise ValueError(s)
        out[tag] = f
    return out


def shares(d, fate, assign="cond", missed=None):
    """Per stand: 2021 live basal area, the part not tallied live in 2026 (cut trees aside), and the share."""
    bsum, lost = {}, {}
    for tag, t in d["live21"].items():
        st = B.cond_stand(d["reg"], t["plot"], t["cond"]) if assign == "cond" else d["reg"][t["plot"]]["Stand"]
        f = fate[tag][0]
        if f == "unknown":
            continue
        b = ba(t["dbh21"])
        bsum[st] = bsum.get(st, 0.0) + b
        if f in ("dead", "missing"):
            lost[st] = lost.get(st, 0.0) + b
    for st, b in (missed or {}).items():
        bsum[st] = bsum.get(st, 0.0) + b
    return {st: dict(b21=bsum[st], lost=lost.get(st, 0.0), share=lost.get(st, 0.0) / bsum[st]) for st in bsum}


def marked(sh):
    return sorted(s for s, v in sh.items() if v["share"] >= W.LINE)


def live26(d, res, dedupe=True):
    out = []
    for r in d["t26"]:
        if r["status"] not in ("L", "N"):
            continue
        if dedupe and r["status"] == "N" and (r["plot"], r["tag"]) in res["dup"]:
            continue
        out.append(r)
    return out


def per_acre(d, recs, area="cond", heights=True, logs_rule="down", tens=True, cull=True, oak=False):
    reg = d["reg"]
    if area == "cond":
        ar = d["areas"]
    else:
        ar = {}
        for p, r in reg.items():
            ar[r["Stand"]] = ar.get(r["Stand"], 0.0) + W.PLOT_AC
    bas, vol = {}, {}
    hw = {k for k, v in d["spp"].items() if v["group"] == "hardwood"}
    for r in recs:
        st = B.cond_stand(reg, r["plot"], r["cond"]) if area == "cond" else reg[r["plot"]]["Stand"]
        bas[st] = bas.get(st, 0.0) + ba(r["dbh"])
        if r["dbh"] < W.SAW_MIN or (r["fia"] in hw and not oak):
            continue
        m = r["merch"]
        if m is None and heights:
            m = d["rev"].get((r["plot"], r["tag"]))
        if not m:
            continue
        q = m / 16.5
        lg = min(6.0, math.floor(q * 2) / 2 if logs_rule == "down" else round(q * 2) / 2)
        if lg < 1:
            continue
        cls = 12 + 2 * int((r["dbh"] - W.SAW_MIN) // 2)
        cls = min(cls, max(d["vol"]))
        g = d["vol"][cls][lg] * (10 if tens else 1)
        vol[st] = vol.get(st, 0.0) + g * ((1 - (r["cull"] or 0) / 100.0) if cull else 1)
    return {st: dict(ba=bas.get(st, 0.0) / a, vol=vol.get(st, 0.0) / a, area=a) for st, a in ar.items()}


def compute(d, **kw):
    res = resolve(d, **{k: v for k, v in kw.items() if k in ("tol", "grow", "centric", "species_check")})
    fate = fates(d, res, kw.get("route", "LINK"))
    sh = shares(d, fate, kw.get("assign", "cond"))
    pa = per_acre(d, live26(d, res, kw.get("dedupe", True)), area=kw.get("area", "cond"),
                  heights=kw.get("heights", True))
    return dict(res=res, fate=fate, shares=sh, marked=marked(sh), pa=pa)


def stand_rows(d, g):
    acres = {r["stand_id"]: int(r["acres"]) for r in d["stands"]}
    rows = []
    for sid in sorted(g["shares"]):
        sh, pa = g["shares"][sid], g["pa"][sid]
        rows.append(dict(stand=sid, acres=acres[sid], share=r1(100 * sh["share"]), ba=r1(pa["ba"]), vol=r10(pa["vol"]),
                         mark=sid in g["marked"]))
    return rows


def write_fates(path, d, g):
    sp = d["spp"]
    alpha2fia = {v["company_code"]: k for k, v in sp.items()}
    rows = []
    for tag, t in d["live21"].items():
        f, t26, d26 = g["fate"][tag]
        rows.append([t["plot"], B.cond_stand(d["reg"], t["plot"], t["cond"]), tag, alpha2fia[t["spp"]],
                     "%.1f" % t["dbh21"], f, t26 if t26 else "", "%.1f" % d26 if d26 is not None else ""])
    rows.sort(key=lambda r: (r[0], r[2]))
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\n")
    wr.writerow(["plot", "stand", "tag_2021", "species_fia", "dbh_2021_in", "fate_2026", "tag_2026", "dbh_2026_in"])
    wr.writerows(rows)
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())
    return len(rows)


def figures(d):
    g = compute(d)
    tag = compute(d, route="TAG")
    excl = compute(d, route="EXCL")
    rows = stand_rows(d, g)
    res = g["res"]
    fv = [v[0] for v in g["fate"].values()]
    fig = {
        "marked": g["marked"], "marked_n": len(g["marked"]), "line_pct": 15,
        "tag_join_marked": tag["marked"], "tag_join_marked_n": len(tag["marked"]),
        "excl_marked": excl["marked"],
        "share_pct": {r["stand"]: "%.1f" % r["share"] for r in rows},
        "ba_ft2_ac": {r["stand"]: "%.1f" % r["ba"] for r in rows},
        "vol_bf_ac": {r["stand"]: "{:,}".format(r["vol"]) for r in rows},
        "tag_join_share_pct": {s: "%.1f" % r1(100 * v["share"]) for s, v in tag["shares"].items()},
        "trees_2021_live": len(d["live21"]), "fates": {k: fv.count(k) for k in ("live", "dead", "missing", "cut")},
        "retagged_linked": len(res["retag"]), "found_tag_duplicates": len(res["dup"]),
        "added_2026": len(res["added"]), "added_new": len(res["new"]),
        "not_found_2026": sum(1 for r in res["rec"].values() if r["status"] == "M"),
        "tolerance_ft": TOL_FT, "ba_constant": W.BA_K, "plot_acres": W.PLOT_AC, "log_ft": 16.5,
        "stands_n": len(rows), "plots_n": len(d["reg"]),
        "policy": W.POLICY_NO, "sawtimber_min_dbh_in": "%.1f" % W.SAW_MIN, "growth_window_in": [GROW[0], GROW[1]],
        "burned_share_pct_range": ["%.1f" % min(r["share"] for r in rows if r["stand"] in W.BURN_DATES),
                                   "%.1f" % max(r["share"] for r in rows if r["stand"] in W.BURN_DATES)],
        "burned_tag_join_pct_range": ["%.1f" % min(r1(100 * tag["shares"][s]["share"]) for s in W.BURN_DATES),
                                      "%.1f" % max(r1(100 * tag["shares"][s]["share"]) for s in W.BURN_DATES)],
        "fire_stand_set_aside_pct": "%.1f" % r1(100 * excl["shares"][W.WILDFIRE[0]]["share"]),
        "next_highest_pct": "%.1f" % max(r["share"] for r in rows if not r["mark"]),
        "retagged_on_burned": sum(1 for t, n in res["retag"].items()
                                  if B.cond_stand(d["reg"], n["plot"], n["cond"]) in W.BURN_DATES),
        "revisit_trees": len(d["rev"]),
    }
    return g, rows, fig


def build(target, gdir, figures_path=None):
    import memo as M
    os.makedirs(gdir, exist_ok=True)
    for f in os.listdir(gdir):
        os.remove(os.path.join(gdir, f))
    d = B.load(target)
    g, rows, fig = figures(d)
    write_fates(os.path.join(gdir, "tree_fates_2021_2026.csv"), d, g)
    M.write(os.path.join(gdir, "salvage_marking_2027.pdf"), d, g, rows, fig)
    if figures_path:
        with open(figures_path, "w", encoding="utf-8") as fh:
            json.dump(fig, fh, indent=1, sort_keys=True)
            fh.write("\n")
    return g, rows, fig
