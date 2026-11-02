"""Write submission.md from generator/figures.json (every figure the write-up states is one the generator computed)."""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def c(n):
    return "{:,}".format(int(n))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    F = P.FILES
    pu, ic, ie = f["pupils"], f["intake_children"], f["intake_entered"]
    fs, fc = f["future_sibling"], f["future_children"]
    text = """## Tags

**Domain:** Sociology & Demography (population projection: a primary school's roll at its next three 1 October counts, each child of its catchment counted by whether a brother or sister is already on the roll).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**De Kwikstaart exceeds its buildings' capacity at the 1 October 2029 count, so the board should request extra accommodation from the 2029-30 school year.** The forecast roll is about {p29} pupils against {cap} places, while the 2027 count ({p27}) and the 2028 count ({p28}) stay within them. Not that the school stays within its places, which counts every coming child at the pooled {rp} per cent of the last five intakes ({pl29} at 2029-30), by neighbourhood ({wk29}) or on the share's trend ({tr29}). Not 2028-29, which counts every catchment child as an entrant ({ev28} at 2028-29).

## 2. Critical Components

1. Of the last five intakes' {itot} catchment children, the {ic1} with a brother or sister from the same household on the roll at their first count entered at **{rs} per cent** ({ie1}) and the {ic0} without one at **{ro} per cent** ({ie0}).
2. The children who first count in 2027, 2028 and 2029 number {f27}, {f28} and {f29}, of whom **{s27}, {s28} and {s29}** have a brother or sister on the 2026 roll still there at their count.
3. The forecast roll is **{p27}, {p28} and {p29}** at the 2027, 2028 and 2029 counts against **{cap}** places.

## 3. Step-by-Step Solution

1. Read {proc} sections 2.3 and 3.1 to 3.5 and {plan}: capacity {cap}, catchment {pc1} and {pc2}, each coming child at the share of the last five intakes' children in its circumstance, taken together.
2. Took each intake's catchment children from {brp} (living there on that 1 October, turned four in the twelve months to it) and matched them to {roll} by birth date, postcode, house number and addition: {ietot} of {itot} entered.
3. Marked a child's circumstance when another member of its household in the register was on the roll at the child's first count: {ie1} of {ic1} such children entered ({rs} per cent), {ie0} of {ic0} others ({ro} per cent).
4. Took the 2026 roll ({roll26} pupils) ageing through group 8 and the out-of-catchment entrants at their five-intake average ({out} a count).
5. Counted the {ftot} catchment children who first count in 2027 to 2029 at their circumstance's share, {fstot} of them with a brother or sister on the 2026 roll still there at their count.
6. For gas, followed the plan's EANs to their buildings' descriptions in {gm} to pick up the dependance's EAN re-registered in January 2025, and took every meter's first and last register in each school year from the 06:00 reads of 1 August in {gr} or the master data's placement and removal readings.
7. For after-school care, kept the locations at Molenwiek 4 in {bl} (BSO-KWS to 11 October, BSO-MLW2 from 12 October) and the De Kwikstaart families in its contracts, and summed the children on each family row of {ba}.
8. Applied 3.5: {x27} and {x28} stay under {cap} and {x29} exceeds it, so the school is short from the 2029-30 count.

## 4. Deliverable Answers

### {book}

1. Short of accommodation: yes, from the 1 October 2029 count (2029-30).
2. Forecast pupils against the capacity of {cap}, to the nearest 10:
   - 2027-28: {p27}, within
   - 2028-29: {p28}, within
   - 2029-30: {p29}, short
3. Entry shares: {rs} per cent with a brother or sister on the roll, {ro} per cent without.
4. Children first counting, and those with a brother or sister on the roll:
   - 1 October 2027: {s27} of {f27}
   - 1 October 2028: {s28} of {f28}
   - 1 October 2029: {s29} of {f29}
5. Column chart of the forecast pupils at each count, the capacity of {cap} drawn as a line.
6. Gas use of both buildings, m3 to the nearest 1,000: 2023-24 {g23}; 2024-25 {g24}; 2025-26 {g25}.
7. After-school care attendances of De Kwikstaart pupils in the dependance, October 2026:
""".format(
        p27=pu["2027"], p28=pu["2028"], p29=pu["2029"], cap=f["capacity"], rp=f["rate_pooled_pct"],
        pl29=int(round(f["pooled_2029"])), wk29=int(round(f["by_wijk_2029"])), tr29=int(round(f["trend_2029"])),
        ev28=int(round(f["everyone_2028"])), itot=c(f["intake_total"]), ic1=ic["True"], ic0=ic["False"],
        ie1=ie["True"], ie0=ie["False"], rs=f["rate_sibling_pct"], ro=f["rate_other_pct"], f27=fc["2027"],
        f28=fc["2028"], f29=fc["2029"], s27=fs["2027"], s28=fs["2028"], s29=fs["2029"], proc=F["procedure"],
        plan=F["accommodation"], pc1=P.CATCHMENT[0], pc2=P.CATCHMENT[1], brp=F["brp"], roll=F["roll"],
        ietot=f["intake_entered_total"], roll26=f["roll_2026"], out=f["out_avg"], ftot=f["future_total"],
        fstot=f["future_sibling_total"], gm=F["gasmaster"], gr=F["gasreads"], bl=F["bso_loc"], ba=F["bso_att"],
        x27=f["pupils_exact"]["2027"], x28=f["pupils_exact"]["2028"], x29=f["pupils_exact"]["2029"],
        book="kwikstaart_leerlingenprognose_2027-2029.docx", g23=c(f["gas_m3"]["2023"]), g24=c(f["gas_m3"]["2024"]),
        g25=c(f["gas_m3"]["2025"]))
    text += "".join("   - %s: %d\n" % (WD[k], f["bso"][str(k)]) for k in range(5))
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
