"""Write submission.md from generator/figures.json (every figure the write-up states is one the generator computed)."""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def c(n):
    return "{:,}".format(int(n))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    F = P.FILES
    H = f["available_m3h"]
    ph, gas = f["phase_flow"], f["gas_m3"]
    h1, ch = f["heat_2425_MWh"], f["heat_change_MWh"]

    def sign(x):
        return ("+" if x > 0 else "") + c(x)
    text = """## Tags

**Domain:** Energy Systems & Utilities (load forecasting: the design-day flow a district heating station must carry as a housing corporation's 1960s blocks leave their gas boiler rooms for the network).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**OS West first runs short of design-day flow in the 2028-29 heating season.** The blocks connected by 1 October 2028 need about {f6} m3/h against the {H} m3/h available, short by about {sh} m3/h, while the 2027-28 blocks fit at about {f3} m3/h. Not that the station holds in both seasons, which carries the blocks at the network's {r0} K design drop, its {r1} K metered drop or the {r2lo} to {r2hi} K of its pre-1985 buildings, drops their original radiators do not make. Not 2027-28, which carries them at the {tb} K drop their radiators were sized for (90/70 C).

## 2. Critical Components

1. The blocks keep their radiators, and the network's original-radiator connections (cold-day returns {rl} to {rh} C, against at most {oh} C for every other connection) make a cold-day drop of **about {d0} K** ({d} K, the mean of their {n} drops).
2. Phases 1 to 3 ({ka} kW) need about **{f3} m3/h** in 2027-28, under the **{H} m3/h** available.
3. Phases 1 to 6 ({kab} kW) need about **{f6} m3/h** in 2028-29, **{sh} m3/h** short.

## 3. Step-by-Step Solution

1. Read {proc} sections 3.2 to 3.4 and {hyd}: a block's design-day flow is its design heat load over {cp} times the drop that connections in service with the same kind of heating installation make on days with a daily mean of 0 C or lower, tested against the {H} m3/h available.
2. Took each complex's design heat loss from {rev} (the most recent study, 3.4) and its phase from {sched}: {ka} kW connected by 2027-28 and {kab} kW by 2028-29.
3. Selected the {cold} days with TG at or below 0 in {wx} and mapped every meter in {amr} to its connection through the Meters sheet of {reg}.
4. The connections' mean cold-day returns split at a gap from {oh} to {rl} C, and the {n} connections above it are the network's original-radiator installations, the kind every block keeps ({scope} section 2: original two-pipe radiators sized for 90/70 C), with a mean cold-day drop of {d} K.
5. Divided each phase's load by {cp} x {d} K: {f3x} m3/h for phases 1 to 3 and {f6x} m3/h for phases 1 to 6.
6. For gas, followed each complex's EAN to its boiler room's description in {gm} to pick up the EANs re-registered in 2026, and took every meter's first and last register in the gas year from the 06:00 reads of 1 October in {gr} or the master data's placement and removal readings.
7. For heat, ran each meter from its annual or connection read in {leg} (GJ or MWh) to its AMR opening register on 1 October 2025, through the drive-by removal reading and the AMR placement reading in the Meters sheet where the meter was exchanged at migration, and took 2025-26 from the AMR registers per meter.
8. Applied 3.3: 2027-28 holds at {f3x} m3/h and 2028-29 needs {f6x} m3/h, {shx} over the {H} available, so OS West first runs short in the 2028-29 heating season.

## 4. Deliverable Answers

### {book}

1. First heating season short: 2028-29.
2. Design-day flow by phase, m3/h to the nearest 5:
   - Phase 1: {p1}
   - Phase 2: {p2}
   - Phase 3: {p3}
   - Phase 4: {p4}
   - Phase 5: {p5}
   - Phase 6: {p6}
3. Blocks connected by the start of each season, m3/h to the nearest 10:
   - 2027-28: {f3} against {H} available, no shortfall
   - 2028-29: {f6} against {H} available, shortfall {sh}
4. Column chart on the Seizoenen sheet: one bar per season (2027-28, 2028-29) labelled with its flow, the available {H} m3/h drawn as a line across both, axis in m3/h.
5. Boiler-room gas from 1 October 2025 to 1 October 2026, m3 to the nearest 1,000:
   - Phase 1: {g1}
   - Phase 2: {g2}
   - Phase 3: {g3}
   - Phase 4: {g4}
   - Phase 5: {g5}
   - Phase 6: {g6}
6. Heat taken by the connections, MWh (residential to the nearest 1,000, utility to the nearest 100):
   - Residential: {hr} in the 2024-25 gas year, {cr} in 2025-26
   - Utility: {hu} in the 2024-25 gas year, {cu} in 2025-26
""".format(
        f3=f["flow_2027_28"], f6=f["flow_2028_29"], sh=f["shortfall_2028_29"], H=H, r0=f["design_drop"],
        r1=f["net_flow"], r2lo=f["pre_res_harm"], r2hi=f["rung_drops"]["r2_pre_hi"], tb=f["textbook_drop"],
        rl=f["return_like_lo"], rh=f["return_like_hi"], oh=f["return_other_hi"], d0=f["drop_K_rounded"], d=f["drop_K"],
        n=f["like_n"], ka=c(f["KA_kW"]), kab=c(f["KAB_kW"]), cp=f["cp"], cold=f["cold_days"],
        f3x=f["flow_2027_28_exact"], f6x=f["flow_2028_29_exact"], shx=f["shortfall_exact"],
        proc=F["procedure"], hyd=F["hydraulic"], rev=F["revised"], sched=F["schedule"], wx=F["weather"], amr=F["amr"],
        reg=F["register"], scope=F["scope"], gm=F["gasmaster"], gr=F["gasreads"], leg=F["legacy"],
        book="os_west_debiet_2027-2029.xlsx",
        p1=ph["1"], p2=ph["2"], p3=ph["3"], p4=ph["4"], p5=ph["5"], p6=ph["6"],
        g1=c(gas["1"]), g2=c(gas["2"]), g3=c(gas["3"]), g4=c(gas["4"]), g5=c(gas["5"]), g6=c(gas["6"]),
        hr=c(h1["Woningen"]), cr=sign(ch["Woningen"]), hu=c(h1["Utiliteit"]), cu=sign(ch["Utiliteit"]))
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
