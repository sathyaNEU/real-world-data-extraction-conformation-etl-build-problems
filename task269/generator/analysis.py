"""The main call from the pack: the default path (the State's study on the 2025 sales as they stand), the rungs below
it, and the golden: the 2026 single-family roll's level and COD measured with the reviewed parcels at their share
and the parcels that did not sell represented by the sold parcels' 2025 values carried forward by their
neighbourhoods' factors. The standing family of that construction is computed beside it."""
import numpy as np
import pandas as pd

import common as K

AS_OF = pd.Timestamp(K.ASSESS_2026)


def cod(r, m):
    return 100.0 * float(np.mean(np.abs(r - m))) / m


def stat(r):
    r = np.asarray(r, float)
    m = float(np.median(r))
    return m, cod(r, m)


def wstat(x, w, how="lower"):
    """Weighted median and COD. lower: the smallest value at which the cumulative weight reaches half; upper: the
    first value past half; mid: the two averaged where the half falls on a boundary."""
    x, w = np.asarray(x, float), np.asarray(w, float)
    o = np.argsort(x, kind="mergesort")
    xs, ws = x[o], w[o]
    cw = np.cumsum(ws) / ws.sum()
    i = int(np.searchsorted(cw, 0.5))
    if how == "upper":
        j = int(np.searchsorted(cw, 0.5, side="right"))
        m = xs[min(j, len(xs) - 1)]
    elif how == "mid" and abs(cw[i] - 0.5) < 1e-12:
        m = (xs[i] + xs[i + 1]) / 2
    else:
        m = xs[i]
    return float(m), 100.0 * float(np.sum(w * np.abs(x - m)) / w.sum()) / float(m)


def sf_frames(pk):
    r26 = pk.roll26[pk.roll26["class_code"] == "R1"].set_index("parcel_id")
    r25 = pk.roll25[pk.roll25["Class"] == "Residential single family"].set_index("pid26")
    return r26, r25


def q_sales(pk, r26, physical=True, carry=True):
    """The 2025 arm's-length single-family sales, set aside where the improvements or boundaries changed after the
    deed (permits finaled, splits and combinations), each price carried to 1 January 2026."""
    d = pk.deeds[(pk.deeds["validation_code"] == "Q") & pk.deeds["pid26"].isin(r26.index)].copy()
    if physical:
        fin = pk.permits.dropna(subset=["final_inspection_date"])
        bad = set()
        for _, p in fin.iterrows():
            bad.add((p["pid26"], p["final_inspection_date"]))
        last_fin = fin.groupby("pid26")["final_inspection_date"].max()
        after = d["pid26"].map(last_fin)
        changed = after.notna() & (after > d["deed_date"]) & (after < AS_OF)
        ch = pk.changes[pk.changes["change_type"].isin(["SPLIT", "COMBINE"])]
        chd = ch.groupby("old_parcel_no")["effective_date"].max()
        after2 = d["parcel_no"].map(chd)
        changed |= after2.notna() & (after2 > d["deed_date"]) & (after2 < AS_OF)
        d = d[~changed]
    d["carry"] = pk.index_carry(d["deed_date"]) if carry else 1.0
    d["price_jan26"] = d["consideration"] * d["carry"]
    d["av26"] = d["pid26"].map(r26["total_assessed_value"])
    d["nbhd"] = d["pid26"].map(r26["nbhd_code"])
    return d


def changes(pk, r26, r25):
    """2025 to 2026 change of every single-family parcel on both rolls under one identifier, with its 2025 sale."""
    both = r26.index.intersection(r25.index)
    ch = pd.DataFrame({"av26": r26.loc[both, "total_assessed_value"], "av25": r25.loc[both, "Total Assessed"],
                       "nbhd": r26.loc[both, "nbhd_code"]})
    ch["chg"] = ch["av26"] / ch["av25"]
    sold = set(pk.deeds.loc[pk.deeds["validation_code"] == "Q", "pid26"])
    ch["sold"] = ch.index.isin(sold)
    return ch


def factors(ch, how="median", exclude=None, county=False):
    u = ch[~ch["sold"]]
    if exclude is not None:
        u = u[~u.index.isin(exclude)]
    if county:
        v = u["chg"].median() if how == "median" else (u["chg"].mean() if how == "mean" else
                                                       u["av26"].sum() / u["av25"].sum())
        return {k: v for k in ch["nbhd"].unique()}
    if how == "median":
        return u.groupby("nbhd")["chg"].median().to_dict()
    if how == "mean":
        return u.groupby("nbhd")["chg"].mean().to_dict()
    g = u.groupby("nbhd")
    return (g["av26"].sum() / g["av25"].sum()).to_dict()


def mixture(study, r25, fac, share, rnd=True, how="lower", post=None):
    av25 = study["pid26"].map(r25["Total Assessed"]).astype(float)
    cf = av25 * study["nbhd"].map(fac)
    if rnd:
        cf = cf.round(-2)
    rc = (cf / study["price_jan26"]).to_numpy()
    ra = (study["av26"] / study["price_jan26"]).to_numpy()
    n = len(study)
    if post is not None:
        wu = study["nbhd"].map(post["unsold_w"]).to_numpy()
        ws = study["nbhd"].map(post["sold_w"]).to_numpy()
        return wstat(np.r_[rc, ra], np.r_[wu, ws], how)
    return wstat(np.r_[rc, ra], np.r_[np.full(n, 1 - share), np.full(n, share)], how)


def main(pk):
    r26, r25 = sf_frames(pk)
    out = {}
    study = q_sales(pk, r26)
    allq = q_sales(pk, r26, physical=False)
    out["study_n"] = len(study)
    out["q_sf_n"] = int((pk.deeds["validation_code"] == "Q").sum())
    sold_ids = set(pk.deeds.loc[pk.deeds["validation_code"] == "Q", "pid26"]) & set(r26.index)
    out["reviewed_n"] = len(sold_ids)
    out["r1_n"] = int(len(r26))
    share = len(sold_ids) / len(r26)
    out["share"] = share
    # rungs
    out["easy"] = stat(study["av26"] / study["price_jan26"])
    out["easy_all_q"] = stat(allq["av26"] / allq["price_jan26"])
    noc = q_sales(pk, r26, carry=False)
    out["no_carry"] = stat(noc["av26"] / noc["price_jan26"])
    allsf = pk.deeds[pk.deeds["pid26"].isin(r26.index) & (pk.deeds["consideration"] > 0)].copy()
    allsf["carry"] = pk.index_carry(allsf["deed_date"])
    allsf["p"] = allsf["consideration"] * allsf["carry"]
    allsf["av26"] = allsf["pid26"].map(r26["total_assessed_value"])
    out["all_deeds"] = stat(allsf["av26"] / allsf["p"])
    jan25 = study["consideration"] * study["deed_date"].map(
        lambda d: pk.idx["2025-01"] / pk.idx["%d-%02d" % (d.year, d.month)])
    out["roll2025_study"] = stat(study["pid26"].map(r25["Total Assessed"]) / jan25)
    # the evidence that the sales do not sample the roll
    ch = changes(pk, r26, r25)
    out["chg_sold"] = float(ch.loc[ch["sold"], "chg"].median())
    out["chg_unsold"] = float(ch.loc[~ch["sold"], "chg"].median())
    out["chg_n_sold"] = int(ch["sold"].sum())
    out["chg_n_unsold"] = int((~ch["sold"]).sum())
    fac = factors(ch)
    out["factors"] = fac
    out["rollfwd"] = stat((study["pid26"].map(r25["Total Assessed"]) * study["nbhd"].map(fac)).round(-2)
                          / study["price_jan26"])
    out["golden"] = mixture(study, r25, fac, share)
    # the standing family
    permit_ids = set(pk.permits["pid26"])
    bor_ids = set(pk.bor["pid26"])
    fam = {}
    fam["neighbourhood median"] = out["golden"]
    fam["neighbourhood mean"] = mixture(study, r25, factors(ch, "mean"), share)
    fam["mean without permit or appeal parcels"] = mixture(study, r25, factors(ch, "mean", permit_ids | bor_ids), share)
    fam["value-weighted change"] = mixture(study, r25, factors(ch, "ros"), share)
    fam["county-wide median change"] = mixture(study, r25, factors(ch, county=True), share)
    fam["unrounded carried values"] = mixture(study, r25, fac, share, rnd=False)
    fam["upper weighted median"] = mixture(study, r25, fac, share, how="upper")
    fam["post-sale-work sales kept"] = mixture(allq, r25, fac, share)
    fam["share on the study's sales"] = mixture(study, r25, fac, len(study) / len(r26))
    popn = r26.groupby("nbhd_code").size()
    sold_nb = r26.loc[r26.index.isin(sold_ids)].groupby("nbhd_code").size().reindex(popn.index, fill_value=0)
    st_nb = study.groupby("nbhd").size().reindex(popn.index, fill_value=0)
    post = {"unsold_w": ((popn - sold_nb) / st_nb).to_dict(), "sold_w": (sold_nb / st_nb).to_dict()}
    fam["post-stratified by neighbourhood"] = mixture(study, r25, fac, share, post=post)
    out["family"] = fam
    return out
