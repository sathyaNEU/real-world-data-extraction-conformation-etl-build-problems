"""The cracker and mirror sheets, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed definition: it dates each delivery by
its proof of delivery and counts customer deliveries only (the prompt and the dictionary say so), joins every
delivery and every report to the facility registry by MFL code for the facility's current region (the battery's
key check finds the registry's repeated codes and keeps the operational record), and sums each facility's approved
report. The mirror stops at the growth-line rung on the call and reads each row's own region (the customer master's
for a delivery, the requisition group's for a report), dating deliveries by their proof of delivery as asked.

Each ask figure is graded at whole bottles: a hit is an exact match. The pair arithmetic is supplemental-stumping
Part 0: a response on the call banks 38 + 7, a response off it 5 + 7, and the asks carry 55.

    python3 cracker.py <pack>      prints the sheet; exit 0 when the pair is at or under 40"""
from __future__ import annotations

import sys

import asks as AS


def figures(P, region_route, date_route, report_route="approved", depot=False, refusals="exclude",
            products="tld_all"):
    a, _ = AS.deliveries(P, region_route, date_route, depot, refusals)
    b, _ = AS.dispensing(P, region_route, report_route, products)
    out = {}
    for (r, c), v in a.items():
        out["delivered %s %s" % (r, c)] = v
    for (r, c), v in b.items():
        out["dispensed %s %s" % (r, c)] = v
    return out


ROUTES = {
    "golden": dict(region_route="registry_dated", date_route="signed"),
    "cracker": dict(region_route="registry_current", date_route="signed", refusals="include", products="cms_code"),
    "mirror": dict(region_route="label", date_route="signed", refusals="include", products="cms_code"),
    "cracker_reissue_cracked": dict(region_route="registry_dated", date_route="signed", refusals="include",
                                    products="cms_code"),
    "cracker_refusals_and_donation_cracked": dict(region_route="registry_current", date_route="signed"),
    "cracker_refusals_cracked": dict(region_route="registry_current", date_route="signed", products="cms_code"),
    "cracker_donation_cracked": dict(region_route="registry_current", date_route="signed", refusals="include"),
    "label_posted": dict(region_route="label", date_route="posted", refusals="include", products="cms_code"),
    "cracker_returns_netted": dict(region_route="registry_current", date_route="signed", refusals="net_returns",
                                   products="cms_code"),
    "cracker_reissue_cracked_returns_netted": dict(region_route="registry_dated", date_route="signed",
                                                   refusals="net_returns", products="cms_code"),
    "cracker_both_A_devices_cracked": dict(region_route="registry_dated", date_route="signed", products="cms_code"),
    "cracker_both_B_devices_cracked": dict(region_route="registry_dated", date_route="signed", refusals="include"),
}


def sheet(pack):
    P = AS.Pack(pack)
    g = figures(P, **ROUTES["golden"])
    res = {}
    for name, kw in ROUTES.items():
        f = figures(P, **kw)
        hits = [k for k in g if f[k] == g[k]]
        res[name] = dict(hits=hits, kept=len(hits) / len(g), n=len(g), fig=f)
    return g, res


def pair(kept_cracker, kept_mirror, on_call_cracker=True, on_call_mirror=False):
    def score(on, kept):
        return (38 + 7 if on else 5 + 7) + 55 * kept
    return (score(on_call_cracker, kept_cracker) + score(on_call_mirror, kept_mirror)) / 2.0


def main(pack):
    g, res = sheet(pack)
    cr, mi = res["cracker"], res["mirror"]
    p = pair(cr["kept"], mi["kept"])
    both = pair(cr["kept"], cr["kept"], True, True)
    print("ask criteria: %d (the table's 24 figures, which the chart's bars carry)" % cr["n"])
    for name, r in res.items():
        print("  %-26s keeps %2d of %d: %s" % (name, len(r["hits"]), r["n"], ", ".join(r["hits"]) or "none"))
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f); both on the call: %.1f" %
          (p, 45 + 55 * cr["kept"], 12 + 55 * mi["kept"], both))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * mi["kept"]))
    return p, res


if __name__ == "__main__":
    p, _ = main(sys.argv[1])
    sys.exit(0 if p <= 40 else 1)
