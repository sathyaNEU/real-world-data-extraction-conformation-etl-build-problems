"""Build task115's bundle: simulate, write target/, recompute the golden from target/, assert.

    python3 build.py            # from task115/generator
"""
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

import claims as CL
import docs
import pack
import seal
import simulate as SIM
import stores as ST
import world as W

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "target"
SEED = W.SEED
# Appendix B of the brief: eleven stores out of the spring cycle, picked by choose_appendix_b so the
# chain-wide multiples are the same with or without them, then frozen before the tune was solved
APPENDIX_B = ["0145", "0161", "0176", "0208", "0251", "0264", "0266", "0276", "0331", "0339", "0342"]


def line_name(item):
    """DELAHUNT ORIGINAL 160S -> Delahunt Original 160s."""
    return re.sub(r"(\d+)S\b", r"\1s", W.LINE[item]["desc"].title()).replace("250G", "250g")


def recap_rows(rows, events, first=dt.date(2025, 1, 1)):
    """Tullan's review figures for each tea cycle: 8 weeks ending two weeks before, stores that ran it."""
    by = defaultdict(dict)
    for (w, sid, item, u, reg, dp, ref) in rows:
        by[(sid, item)][w] = (u, dp)
    out = []
    for code, start, item, kind, val, label in events:
        if start < first:
            continue
        cw = [start + dt.timedelta(days=7 * k) for k in range(3)]
        bw = [start - dt.timedelta(days=7 * k) for k in range(2, 10)]
        ran = [sid for (sid, it), wk in by.items() if it == item and all(w in wk and wk[w][1] is not None for w in cw)]
        base, ev = 0.0, 0.0
        for sid in ran:
            wk = by[(sid, item)]
            vals = [wk[w][0] for w in bw if w in wk and wk[w][1] is None]
            if not vals:
                continue
            base += sum(vals) / len(vals)
            ev += sum(wk[w][0] for w in cw) / 3
        out.append({"code": code, "start": start, "item": item, "label": label, "stores": len(ran),
                    "base": base, "deal": ev, "mult": ev / base})
    return out


def choose_appendix_b(rows, stores, seed):
    """Eleven stores out of the spring cycle, chosen so the chain's forecast multiples do not move."""
    rng = np.random.default_rng(seed * 19 + 1)
    base_w = set(W.BASE_WEEKS)
    acc = defaultdict(list)
    for (w, sid, item, u, reg, dp, ref) in rows:
        if w in base_w and dp is None and item in (W.DEL160, W.OL160):
            acc[(sid, item)].append(u)
    pf = {}
    for s in stores:
        for w in W.BASE_WEEKS:
            sid = ST.scan_ids(s, w)
            if sid:
                pf[sid] = s
    sids = sorted({k[0] for k in acc})
    b = {s: np.mean(acc[(s, W.DEL160)]) for s in sids}
    o = {s: np.mean(acc[(s, W.OL160)]) for s in sids}

    def mult(excl, menu):
        num = den = 0.0
        for s in sids:
            if s in excl:
                continue
            st = pf[s]
            reg = W.PRICE[W.DEL160][st["pfile"]][1]
            olp = W.PRICE[W.OL160][st["pfile"]][1]
            k, v = menu
            dp = W.deal_price(reg, k, v)
            num += b[s] * (1 + W.lift(W.depth(reg, k, v))) + (W.SWITCH_GAIN * o[s] if dp <= olp else 0)
            den += b[s]
        return num / den
    full = {m: mult(set(), (k, v)) for m, k, v, lab in W.MENU}
    cand = [s for s in sids if s not in ("0119", "0388", "0203", "0256", "0377")]
    best = None
    for _ in range(20000):
        pick = set(rng.choice(cand, 11, replace=False))
        regs = {pf[s]["reg_event"] for s in pick}
        if len(regs) < 4:
            continue
        err = max(abs(mult(pick, (k, v)) - full[m]) for m, k, v, lab in W.MENU)
        if best is None or err < best[0]:
            best = (err, sorted(pick))
        if err < 0.0004:
            break
    return best


def main():
    stores = ST.build(SEED)
    rows, means, truth = SIM.simulate(stores, SEED)
    returns = CL.island_returns(stores, SEED)
    flines, dn, cmeta = CL.build_claims(rows, stores, returns, SEED)
    TARGET.mkdir(exist_ok=True)
    for p in TARGET.iterdir():
        if p.is_file():
            p.unlink()
    nfeed = pack.write_feed(rows, TARGET)
    pack.write_lines(TARGET)
    pack.write_calendar(TARGET)
    nmem = pack.write_members(stores, TARGET)
    pack.write_claims(flines, dn, returns, TARGET)
    rec = recap_rows(rows, W.EVENTS, first=dt.date(2024, 1, 1))
    # Delahunt's own reviews: its cycles, Tullan's figures, funding as invoiced
    fund = defaultdict(float)
    for (w, sid, item, u, reg, dp, ref) in rows:
        if ref and W.LINE[item]["supplier"] == "Delahunt Tea":
            fund[ref] += u * (reg - dp)
    for d in dn:
        if d["Cycle"] == "BD26-04":
            fund["BD26-04"] = d["Net (EUR)"]
    reviews = []
    for r in rec:
        if W.LINE[r["item"]]["supplier"] != "Delahunt Tea" or r["code"] == "BD26-13" or r["start"].year < 2025:
            continue
        cw = [r["start"] + dt.timedelta(days=7 * k) for k in range(3)]
        bw = [r["start"] - dt.timedelta(days=7 * k) for k in range(2, 10)]
        reviews.append([r["code"], line_name(r["item"]), r["label"],
                        "w/c %s to w/c %s" % (cw[0].strftime("%d %b %Y"), cw[-1].strftime("%d %b %Y")),
                        "w/c %s to w/c %s" % (bw[-1].strftime("%d %b %Y"), bw[0].strftime("%d %b %Y")),
                        round(r["base"]), round(r["deal"]), round(r["mult"], 2), round(fund[r["code"]], 2),
                        "R. Masterson"])
    pack.write_reviews(reviews, TARGET)
    appb = APPENDIX_B
    byno = {}
    for s in stores:
        byno.setdefault(s["no"], s)
        if s.get("renumbered_to"):
            byno[s["renumbered_to"]] = s
    sw = next(s for s in stores if s["no"] == "0119" and s.get("reissued"))
    byno["0119"] = sw
    reasons = ["Refit, closed 22 February to 28 March 2027"] * 4 + \
              ["Refit, trading from a temporary unit with no leaflet space"] * 2 + \
              ["Leaving the group on 27 February 2027"] * 3 + ["Relocating to new premises in March 2027"] * 2
    appendix = [[s, byno[s]["name"], reasons[i]] for i, s in enumerate(appb)]
    docs.brief(TARGET / "Big_Deals_Spring_2027_supplier_brief.docx", appendix)
    moves = []
    for s in sorted(stores, key=lambda x: x["no"]):
        if s.get("history_only") or not s["scanning"]:
            continue
        no = s.get("renumbered_to", s["no"]) if s.get("renumbered_to") else s["no"]
        if s.get("reissued"):
            continue
        if s["reg_event"] != s["reg_jan"]:
            moves.append([no, s["name"], docs.REG[s["reg_jan"]], docs.REG[s["reg_event"]], "6 July 2026"])
    for s in sorted(stores, key=lambda x: x["no"]):
        if s.get("history_only") or not s["scanning"] or s.get("reissued"):
            continue
        if s["reg_may27"] != s["reg_event"]:
            moves.append([s.get("renumbered_to", s["no"]), s["name"], docs.REG[s["reg_event"]],
                          docs.REG[s["reg_may27"]], "3 May 2027"])
    docs.area_notice(TARGET / "tullan_area_structure_from_6_July_2026.docx", moves)
    changes = [["0147", "New store number", "Tullan Phibsborough trades as store 0388 from 6 April 2026."],
               ["0119", "Left the group", "Tullan Ballinrobe left the group on 31 May 2026."],
               ["0119", "Opened", "Tullan Swords Rivervalley opened on 3 August 2026, trading region Dublin & North East."]]
    docs.member_news(TARGET / "member_news_2026.docx", changes)
    rv = []
    for r in rec:
        if r["start"] < dt.date(2025, 1, 1):
            continue
        cw = [r["start"] + dt.timedelta(days=7 * k) for k in range(3)]
        rv.append([r["code"], "%s to %s" % (cw[0].strftime("%d %b"), (cw[-1] + dt.timedelta(days=6)).strftime("%d %b %Y")),
                   line_name(r["item"]),
                   r["label"], r["stores"], "{:,}".format(round(r["base"])), "{:,}".format(round(r["deal"])),
                   "%.2f" % r["mult"]])
    uses = defaultdict(int)
    for r in rec:
        if r["start"] >= dt.date(2025, 1, 1):
            uses[r["label"]] += 1
    top = max(rec, key=lambda r: r["mult"])
    most = max(uses.items(), key=lambda kv: kv[1])
    assert sorted(uses.values())[-2] < most[1]
    words = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}
    notes = ["%s was the mechanic we ran most, in %s cycles. The strongest single cycle was %s %s in %s, at "
             "%.2f times base." % (most[0], words[most[1]], W.LINE[top["item"]]["desc"].title().replace("160S", "160s")
                                   .replace("80S", "80s"), top["label"], top["start"].strftime("%B %Y"),
                                   top["mult"])]
    docs.review_pdf(TARGET / "big_deals_review_tea_2025-26.pdf", rv, notes)
    docs.rrp_pdf(TARGET / "tullan_own_brand_rrp_2026.pdf")
    docs.feed_spec_pdf(TARGET / "TullanInsight_category_feed_v3_spec.pdf")
    docs.thread(TARGET / "delahunt_commercial_thread_oct2026.txt")
    docs.readme(TARGET / "README_tullan_spring_2027.txt", {"feed": "{:,}".format(nfeed), "members": nmem,
                                                           "claims": "{:,}".format(len(flines))})
    seal.seal_dir(TARGET, seal.TARGET)
    state = {"appendix_b": appb, "wrong": cmeta["wrong"], "late": cmeta["late"]}
    return stores, rows, state


if __name__ == "__main__":
    stores, rows, state = main()
    print("appendix B", state["appendix_b"])
