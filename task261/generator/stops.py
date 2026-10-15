"""The asks computed from the shipped insurer files the way each kind of response would (the ask sheet's stops and the
cracker's path), for checks.py."""
from __future__ import annotations

import os

import pandas as pd

import common as K

AS = pd.Timestamp(K.AS_AT)
RATE = {"CPI": 0.031, "Fixed 2.5%": 0.025, "Level": 0.0}


class Files:
    def __init__(self, folder):
        self.crm = pd.read_csv(os.path.join(folder, K.CRM), dtype=str)
        self.crm["date_of_birth"] = pd.to_datetime(self.crm["date_of_birth"])
        self.crm["date_of_death"] = pd.to_datetime(self.crm["date_of_death"])
        self.crm["age"] = K.AS_AT.year - self.crm["date_of_birth"].dt.year
        self.acc = pd.read_csv(os.path.join(folder, K.RIA), dtype={"account_no": str, "member_id": str})
        self.nom = pd.read_csv(os.path.join(folder, K.NOMS), dtype={"account_no": str},
                               parse_dates=["nominee_date_of_birth"])
        self.ann = pd.read_csv(os.path.join(folder, K.ANN), dtype={"contract_no": str, "client_id": str},
                               parse_dates=["date_of_birth", "date_of_death", "commenced", "payments_start"])
        self.by = self.crm.set_index("client_id")
        self.merge = self.by["merged_into"].dropna()
        self.members = self.crm[self.crm.status != "Merged"].groupby("household_id")["client_id"].apply(list)
        self.rev = self.nom[self.nom.nomination_type == "Reversionary"]
        self.sp = self.nom[self.nom.relationship.isin(["Spouse", "De facto partner"])]
        self.revset = set(self.rev.account_no)

    def resolve(self, cid, follow=True):
        return self.merge[cid] if (follow and cid in self.merge.index) else cid

    def alive31(self, cid):
        d = self.by.at[cid, "date_of_death"]
        return pd.isna(d) or d > AS

    def status_alive(self, cid):
        return self.by.at[cid, "status"] != "Deceased"

    def house(self, cid, rule):
        hh = self.by.at[cid, "household_id"]
        ms = self.members.get(hh, [cid]) if self.by.at[cid, "status"] != "Merged" else [cid]
        if rule == "all":
            return ms
        if rule == "status":
            return [m for m in ms if self.status_alive(m)]
        return [m for m in ms if self.alive31(m)]


def ask_a(F, follow=True, keep_dead_owner=False, life="alive31", nominee=False, revert=False):
    out = {g: [set(), 0.0, 0.0] for g in range(6)}
    owners = F.acc.member_id.map(lambda x: F.resolve(x, follow))
    for a, cid in zip(F.acc.itertuples(), owners):
        if cid not in F.by.index:
            continue
        ok = F.alive31(cid) if life == "alive31" else (F.status_alive(cid) if life == "status" else True)
        if ok:
            ms = F.house(cid, life)
            ms = ms if cid in ms else ms + [cid]
            ages = [F.by.at[m, "age"] for m in ms]
            key = ("hh", F.by.at[cid, "household_id"])
            if nominee and len(F.house(cid, "all")) == 1:
                sp = F.sp[F.sp.account_no.isin(F.acc.loc[owners == cid, "account_no"])]
                if len(sp):
                    ages.append(K.AS_AT.year - sp.nominee_date_of_birth.iloc[0].year)
        elif revert and a.account_no in F.revset:
            nd = F.rev.loc[F.rev.account_no == a.account_no, "nominee_date_of_birth"].iloc[0]
            ms = [m for m in F.house(cid, "alive31") if m != cid]
            ages = [F.by.at[m, "age"] for m in ms] if ms else [K.AS_AT.year - nd.year]
            key = ("hh", F.by.at[cid, "household_id"]) if ms else ("rev", a.account_no)
        elif keep_dead_owner:
            ms = F.house(cid, "all")
            ages = [F.by.at[m, "age"] for m in ms]
            key = ("hh", F.by.at[cid, "household_id"])
        else:
            continue
        g = int(K.band_of(max(ages)))
        out[g][0].add(key)
        out[g][1] += a.balance_31_12_2026
        out[g][2] += a.annual_payment_2026_27
    return {g: dict(households=len(v[0]), balance=v[1], payments=v[2]) for g, v in out.items()}


def ask_b(F, life="alive31", in_payment=False, deflate=False, nominee=False, deferred=False):
    out = {g: [set(), 0.0] for g in range(6)}
    c = F.ann[F.ann.commenced <= AS].copy()
    if deferred:
        c = c[c.payments_start <= AS]
    c["a31"] = c.date_of_death.isna() | (c.date_of_death > AS)
    c["anow"] = c.life_status == "Alive"
    flag = "a31" if life == "alive31" else "anow"
    owners = F.acc.member_id.map(F.resolve)
    for k, grp in c.groupby("contract_no"):
        lives = grp[grp[flag]].sort_values("life_no")
        if not len(lives):
            continue
        if in_payment:
            lives = lives.iloc[:1]
        amt = lives.annual_amount.sum()
        if deflate:
            s = grp.commenced.iloc[0]
            if s.month == 1 and s.day <= K.PULL.day:
                ann_day = pd.Timestamp(2027, 1, s.day)
                lv = lives.iloc[0]
                if lv.life_no == 2 or pd.isna(lv.date_of_death) or lv.date_of_death > ann_day:
                    amt = amt / (1 + RATE[grp.indexation.iloc[0]])
        pay = lives.iloc[0].client_id
        ms = F.house(pay, "alive31" if life == "alive31" else "status")
        ms = ms if pay in ms else ms + [pay]
        ages = [F.by.at[m, "age"] for m in ms]
        if in_payment and len(grp) == 2:
            other = grp[grp.life_no != lives.iloc[0].life_no]
            if len(other) and bool(other[flag].iloc[0]):
                ages.append(K.AS_AT.year - other.date_of_birth.iloc[0].year)
        if nominee and len(F.house(pay, "all")) == 1 and not (in_payment and len(grp) == 2):
            sp = F.sp[F.sp.account_no.isin(F.acc.loc[owners == pay, "account_no"])]
            if len(sp):
                ages.append(K.AS_AT.year - sp.nominee_date_of_birth.iloc[0].year)
        g = int(K.band_of(max(ages)))
        out[g][0].add(F.by.at[pay, "household_id"])
        out[g][1] += amt
    return {g: dict(households=len(v[0]), income=v[1]) for g, v in out.items()}


A_STOPS = {"naive": dict(follow=False, keep_dead_owner=True, life="all"),
           "status": dict(life="status"),
           "cracker": dict(nominee=True),
           "register only": dict(),
           "reversion only": dict(revert=True),
           "golden": dict(nominee=True, revert=True)}
B_STOPS = {"alive now, every life": dict(life="now"),
           "cracker": dict(nominee=True),
           "every life summed, register only": dict(),
           "deferred out": dict(deferred=True),
           "every life summed, deferred out": dict(deferred=True, deflate=True, nominee=True),
           "in payment, deferred out": dict(in_payment=True, deferred=True),
           "January increase kept": dict(in_payment=True, deferred=True, nominee=True),
           "nominations unread": dict(in_payment=True, deflate=True, deferred=True),
           "deferred kept": dict(in_payment=True, deflate=True, nominee=True),
           "golden": dict(in_payment=True, deflate=True, nominee=True, deferred=True)}
