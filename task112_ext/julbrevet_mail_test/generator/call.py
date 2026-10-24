# Independent reproduction of the frozen main call from the shipped inputs.
import sys, pandas as pd, numpy as np
from scipy import stats
D = sys.argv[1]
crm = pd.read_csv(f"{D}/crm_members_extract_2028-01-08.csv", dtype=str)
crm['joined_date'] = pd.to_datetime(crm['joined_date']); crm['closed_date'] = pd.to_datetime(crm['closed_date'])
msm = pd.read_csv(f"{D}/member_store_month_2027.csv", dtype={'member_id':str,'month':str,'store_code':str})
dm = pd.read_csv(f"{D}/direct_mail_drops_2027.csv", dtype=str)
snap = pd.read_csv(f"{D}/consent_snapshot_2026-01-01.csv", dtype=str)
ev = pd.read_csv(f"{D}/consent_events_2026-2027.csv", dtype=str)
sel = pd.Timestamp('2027-11-15')
open_sel = crm[(crm.joined_date <= sel) & (crm.closed_date.isna() | (crm.closed_date >= sel))]
print('accounts open on selection date', len(open_sel), 'households', open_sel.household_id.nunique())
m2h = crm.set_index('member_id').household_id
msm['hh'] = msm.member_id.map(m2h)
print('msm rows with no crm member', msm.hh.isna().sum())
jo = msm[msm.month.between('2027-01','2027-10')].groupby('hh').spend_sek.sum()
hh_open = open_sel.household_id.unique()
elig = [h for h in hh_open if jo.get(h,0) >= 6000]
elig = pd.Index(elig)
print('eligible households', len(elig))
# main card holder: earliest-joined open account on selection date
mch = open_sel.sort_values(['joined_date','member_id']).groupby('household_id').first()
# consent post state at selection 2027-11-14 23:00 UTC
cut = pd.Timestamp('2027-11-14 23:00:00')
ev['t'] = pd.to_datetime(ev.event_time_utc.str.replace('Z','')); evp = ev[(ev.channel=='post') & (ev.t < cut)].sort_values(['t','event_id'])
state = snap.set_index('member_id').post.to_dict()
for r in evp.itertuples(): state[r.member_id] = 'Y' if r.action=='granted' else 'N'
def post_ok(m): return state.get(m,'N')
jul = dm[dm.drop_code=='BV27-13-D1']
mailed = pd.Index(jul.household_id.unique())
print('mailed households', len(mailed), 'areas', jul.postcode_area.nunique(), 'rows', len(jul))
hh_area = crm.groupby('household_id').postcode_area.first()
held = sorted(set(hh_area.loc[elig].unique()) - set(jul.postcode_area.unique()))
print('held-back areas', held)
elig_held = [h for h in elig if hh_area[h] in held]
obj = [h for h in elig if post_ok(mch.loc[h,'member_id'])!='Y']
ctrl = [h for h in elig_held if post_ok(mch.loc[h,'member_id'])=='Y']
print('eligible in held areas', len(elig_held), 'control', len(ctrl), 'objectors all areas', len(obj), 'objectors in held', len(elig_held)-len(ctrl))
print('mailed subset of eligible?', set(mailed) <= set(elig), 'mailed & objectors', len(set(mailed)&set(obj)))
dec = msm[msm.month=='2027-12'].groupby('hh').spend_sek.sum()
def grp(hs): v = np.array([dec.get(h,0.0) for h in hs]); return len(v), v.mean()
for name,hs in [('mailed',mailed),('control',ctrl),('objected',obj)]:
    n,mu = grp(hs); print(f"{name}: {n} households, {mu:.2f} SEK")
# cluster interval
df = pd.DataFrame({'hh': list(mailed)+ctrl, 'g': [1]*len(mailed)+[0]*len(ctrl)})
df['y'] = [dec.get(h,0.0) for h in df.hh]; df['area'] = hh_area.loc[df.hh].values
diff = df[df.g==1].y.mean() - df[df.g==0].y.mean()
a = df.groupby(['g','area']).agg(n=('y','size'), m=('y','mean')).reset_index()
def wvar(sub):
    w = sub.n/sub.n.sum(); mu = (w*sub.m).sum(); k = len(sub)
    # variance of weighted mean of cluster means, CR-style
    return mu, (k/(k-1))*((w**2)*(sub.m-mu)**2).sum(), k
m1,v1,k1 = wvar(a[a.g==1]); m0,v0,k0 = wvar(a[a.g==0])
se = np.sqrt(v1+v0); dfw = (v1+v0)**2/(v1**2/(k1-1)+v0**2/(k0-1)); t = stats.t.ppf(0.95, dfw)
print(f"diff {diff:.2f}; wmeans {m1:.2f} {m0:.2f}; se {se:.2f}; df {dfw:.2f}; t {t:.4f}; range {diff-t*se:.2f} {diff+t*se:.2f}")
lo = diff - t*se; print('lower margin', round(0.25*lo,2), 'shortfall', round(11.40-0.25*lo,2), 'needed', round(45.60+t*se,2))
