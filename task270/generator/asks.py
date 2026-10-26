"""The asks for task270, each device's handling a switch so the golden, the cracker and the checks run one path:
each region's HFC packs' full charge in tonnes of CO2 equivalent, all and on R404A (each pack at the refrigerant it
held in 2026, which the job sheets carry and the register does not always), and each region's refrigerant charged in 2026 into its integral
cabinets and cold rooms (a job's kilograms as the cylinder it came from lost them, the handheld having stamped some
jobs' totals on every asset line)."""
import pandas as pd

import analysis as A
import common as K


def pack_gas(target, P, J, source="jobs"):
    """the refrigerant each pack held in 2026: the latest 2024 to 2026 job sheet's refrigerant (a retrofit's new
    blend), or the register's"""
    if source == "register":
        return P["gas"]
    j = J.sort_values("date")
    last = j.groupby("code")["refrigerant"].last().map(A.gas)
    return last.reindex(P.index).fillna(P["gas"])


def charge_co2e(target, P, J, source="jobs"):
    """each region's HFC packs' full charge in tonnes of CO2 equivalent, all packs and the packs on R404A"""
    g = pack_gas(target, P, J, source)
    t = P["charge"] * g.map(K.GWP) / 1000.0
    allp = t.groupby(P["region"]).sum().reindex(K.REGIONS).fillna(0.0)
    r404 = t[g == "R404A"].groupby(P["region"][g == "R404A"]).sum().reindex(K.REGIONS).fillna(0.0)
    return allp, r404


def equipment_charges(target, mode="cylinder"):
    """refrigerant charged in 2026 into integral cabinets and cold rooms, by region; mode cylinder reads each job's
    kilograms from the cylinder log, lines sums the job sheet's asset lines"""
    J = A.jobs(target)
    E = A.read(target, "register", sheet="Cabinets and cold rooms")
    S = A.read(target, "stores")
    code = {v: k for k, v in K.REGION_NAME.items()}
    reg = dict(zip(S["store_no"].astype(int), S["region"].map(code)))
    eq = set(E["Asset"])
    j = J[(J["date"].dt.year == K.YEAR) & J["asset"].isin(eq)].copy()
    j["region"] = j["store"].astype(int).map(reg)
    if mode == "lines":
        return j.groupby("region")["charged_kg"].sum().reindex(K.REGIONS).fillna(0.0)
    C = A.read(target, "cylinders")
    C["used"] = C["gross_before_kg"].astype(float) - C["gross_after_kg"].astype(float)
    used = C.groupby("job_no")["used"].sum()
    per_job = j.groupby("job_no").agg(region=("region", "first"))
    per_job["kg"] = used.reindex(per_job.index).fillna(0.0)
    return per_job.groupby("region")["kg"].sum().reindex(K.REGIONS).fillna(0.0)


def all_asks(target, L=None, P=None, J=None, gas_source="jobs", eq_mode="cylinder"):
    if P is None:
        P = A.packs(target)
    if J is None:
        J = A.pack_jobs(target, P)
    if L is None:
        L = A.losses(target, P=P, J=J)
    allp, r404 = charge_co2e(target, P, J, gas_source)
    e = equipment_charges(target, eq_mode)
    return dict(charge_co2e_t={k: K.r(v) for k, v in allp.items()}, r404a_co2e_t={k: K.r(v) for k, v in r404.items()},
                equipment_kg={k: K.r(v, 1) for k, v in e.items()})
