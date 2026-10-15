"""The State Office of the Medical Examiner's review of the 2025 deaths the department listed: every county resident's
2025 death on the closed 2025 file whose underlying cause was a drug poisoning, each read against the full case file
and toxicology, with the drugs that caused or contributed and the drugs present that did not."""
import datetime as dt

import deaths as DE
import world as W

DAY = dt.timedelta(days=1)
STIM = {"methamphetamine", "amphetamine", "cocaine"}
OPI = set(DE.OPIOIDS)
NICE = {"delta-9-THC": "delta-9-tetrahydrocannabinol", "opioid, unspecified": "opioid (unspecified)"}


def _name(x):
    return NICE.get(x, x)


STYLE = {
    "AME-1": ("Acute %s toxicity", "Acute combined %s toxicity", "; ethanol intoxication contributing"),
    "AME-2": ("%s intoxication", "Mixed drug intoxication (%s)", "; acute ethanol intoxication"),
    "AME-3": ("Toxic effects of %s", "Combined toxic effects of %s", " with ethanol"),
    "AME-4": ("%s toxicity", "Multiple drug toxicity: %s", "; ethanol contributing"),
}
LOAD = [("AME-1", .34), ("AME-2", .27), ("AME-3", .23), ("AME-4", .16)]


def _cause(d, who):
    one, many, eth_txt = STYLE[who]
    c = [_name(x) for x in d["contrib"] if x != "ethanol"]
    if len(c) == 1:
        text = one % c[0]
    elif who == "AME-1" or who == "AME-3":
        text = many % (", ".join(c[:-1]) + " and " + c[-1])
    else:
        text = many % ", ".join(c)
    text = text[0].upper() + text[1:]
    if "ethanol" in d["contrib"]:
        text += eth_txt
    if d["cls"] == "S" and "I25.1" in d["axis"]:
        text += "; hypertensive and atherosclerotic cardiovascular disease contributing"
    return text


def _assign(reviewed):
    """The pathologists take the department's list in blocks, each finishing a block over a week or two."""
    h = DE.rng("review_blocks")
    cum = [sum(p for _, p in LOAD[:i + 1]) for i in range(len(LOAD))]
    span = (W.REVIEW_DONE - W.REVIEW_LIST).days - 48
    out, i = {}, 0
    order = sorted(reviewed, key=lambda d: d["sfn"])
    while i < len(order):
        n = int(h.integers(6, 19))
        u = h.random()
        who = next(r for (r, _), c in zip(LOAD, cum) if u < c)
        start = W.REVIEW_LIST + (24 + int(h.integers(0, span))) * DAY
        for d in order[i:i + n]:
            out[d["sfn"]] = (who, start + int(h.integers(0, 15)) * DAY)
        i += n
    return out


def rows(final):
    reviewed = sorted([d for d in final if d["year"] == W.REVIEW_YEAR], key=lambda d: d["sfn"])
    g = DE.rng("review")
    work = _assign(reviewed)
    out = []
    coroner_seq = {}
    for i, d in enumerate(sorted(reviewed, key=lambda d: (d["dod"], d["sfn"]))):
        office = {"county": "WC", "state": {"Varnholt": "VC", "Ardemere": "AC", "Quillon": "QC"}.get(d["occ_county"], "SC")}.get(
            d["place_kind"], d["occ_state"])
        coroner_seq[office] = coroner_seq.get(office, 0) + 1 + int(g.integers(0, 3))
        case = "%s25-%04d" % (office, coroner_seq[office]) if d["place_kind"] != "out" else "%s-25-%05d" % (office, 1000 + 7 * coroner_seq[office])
        who, done = work[d["sfn"]]
        out.append({
            "review_id": "OME-R25-%04d" % (i + 1),
            "state_file_no": d["sfn"],
            "case_number": case,
            "date_of_death": d["dod"].isoformat(),
            "age": d["age"],
            "sex": d["sex"],
            "cause_of_death": _cause(d, who),
            "drugs_caused_or_contributed": "; ".join(_name(x) for x in d["contrib"]),
            "drugs_present_not_contributing": "; ".join(_name(x) for x in d["present"]),
            "opioid_caused_or_contributed": "Y" if any(x in OPI for x in d["contrib"]) else "N",
            "manner": d["manner"],
            "review_completed": done.isoformat(),
            "reviewer": who,
        })
    out.sort(key=lambda r: r["review_id"])
    return out
