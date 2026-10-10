"""The CRM and network extracts, written in the layout the data platform exports them in."""
import datetime as dt
import numpy as np
import pandas as pd

import world as W

CANTON = {"SGS": "SG", "FUE": "SG", "RHT": "SG", "TGO": "TG", "TOG": "SG", "APZ": "AR"}


def facts_frame(sim):
    ci, wi = np.nonzero(sim["spend"] > 0)
    rng = np.random.default_rng(W.SEED + 7)
    spend = sim["spend"][ci, wi]
    baskets = np.maximum(1, rng.poisson(spend / 41.0)).astype(np.int16)
    df = pd.DataFrame({
        "card_no": sim["cards"][ci],
        "iso_week": np.array(W.WEEKS)[wi],
        "week_start": [W.WEEK_START[w] for w in np.array(W.WEEKS)[wi]],
        "baskets": baskets,
        "gross_sales_chf": spend,
        "gross_margin_chf": sim["margin"][ci, wi],
        "reward_cost_chf": sim["reward"][ci, wi],
    })
    df = df.sort_values(["iso_week", "card_no"], kind="mergesort").reset_index(drop=True)
    return df


def allocation_frame(sim):
    rng = np.random.default_rng(W.SEED + 11)
    from sim import allocation_bucket
    t0 = pd.Timestamp("2026-05-26 04:40:00")
    secs = np.sort(rng.integers(0, 3 * 3600, len(sim["cards"])))
    order = rng.permutation(len(sim["cards"]))
    df = pd.DataFrame({
        "card_no": sim["cards"][order],
        "test_code": "ST26",
        "cell": sim["cell"][order],
        "bucket": [allocation_bucket(c) for c in sim["cards"][order]],
        "allocated_at": (t0 + pd.to_timedelta(secs, unit="s")).strftime("%Y-%m-%d %H:%M:%S"),
        "engine_release": "OE 4.2.1",
    })
    return df


def cards_frame(sim):
    rng = np.random.default_rng(W.SEED + 13)
    n = len(sim["cards"])
    joined = sim["joined"][sim["m_idx"]]
    lag = pd.to_timedelta(np.where(sim["pos"] == 0, 0, rng.integers(30, 4000, n)), unit="D")
    issued = pd.Series(joined + lag).clip(upper=pd.Timestamp("2026-03-28"))
    reissue = rng.random(n) < 0.22
    issued = issued.where(~reissue, issued + pd.to_timedelta(rng.integers(200, 2500, n), unit="D")).clip(
        upper=pd.Timestamp("2026-03-28"))
    channel = rng.choice(["branch", "app", "post"], n, p=[0.58, 0.27, 0.15])
    app = np.where(rng.random(n) < np.where(sim["pos"] == 0, 0.61, 0.44), "Y", "N")
    df = pd.DataFrame({
        "card_no": sim["cards"],
        "membership_no": sim["memb_no"][sim["m_idx"]],
        "card_type": np.where(sim["pos"] == 0, "main", "additional"),
        "issued_on": issued.dt.strftime("%Y-%m-%d"),
        "issue_channel": channel,
        "app_linked": app,
        "card_status": "active",
    })
    df = df.sort_values(["membership_no", "card_type", "issued_on"], ascending=[True, False, True]).reset_index(drop=True)
    return df


def memberships_frame(sim):
    rng = np.random.default_rng(W.SEED + 17)
    bmap = {b[0]: b for b in W.BRANCHES}
    pcode = [bmap[h][3] for h in sim["home"]]
    n = len(sim["home"])
    # a member's postcode is usually the branch's own or a neighbouring one
    jitter = rng.choice([0, 0, 0, 1, 2, 5, 10], n)
    postcode = [str(int(p) + int(j)) for p, j in zip(pcode, jitter)]
    canton = [CANTON[W.region_january(h)] for h in sim["home"]]
    df = pd.DataFrame({
        "membership_no": sim["memb_no"],
        "member_since": pd.Series(sim["joined"]).dt.strftime("%Y-%m-%d"),
        "home_branch": sim["home"],
        "postcode": postcode,
        "canton": canton,
        "correspondence_lang": rng.choice(["de", "de", "de", "de", "it", "fr", "en"], n),
        "share_certificates": rng.choice([1, 1, 1, 1, 2, 3], n),
        "newsletter": np.where(rng.random(n) < 0.47, "Y", "N"),
    })
    return df.sort_values("membership_no").reset_index(drop=True)


def branches_frame():
    rows = []
    for b in W.BRANCHES:
        rows.append({
            "branch_no": b[0], "branch_name": b[1], "town": b[2], "postcode": b[3],
            "region_code": b[4], "region_name": W.REGION_NAME[b[4]], "format": b[5],
            "opened_on": b[6], "area_manager": AREA_MANAGER[b[4]],
        })
    return pd.DataFrame(rows)


AREA_MANAGER = {"SGS": "Amelie Peter", "FUE": "Nemanja Scheidegger", "RHT": "Enis Stutz",
                "TGO": "Ursula Wehrli", "TOG": "Ludwig Gfeller", "APZ": "Aline Baur"}


def region_2027_of_membership(mem):
    return mem.set_index("membership_no")["home_branch"].map(W.region_2027)


def region_january_of_membership(mem):
    return mem.set_index("membership_no")["home_branch"].map(W.region_january)
