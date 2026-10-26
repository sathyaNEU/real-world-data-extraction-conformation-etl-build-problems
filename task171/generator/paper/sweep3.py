import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sim_er3 as S

n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
if len(sys.argv) > 2:
    S.P.update(json.loads(sys.argv[2]))
clean = [('d14', 'none'), ('d14', 'strat'), ('d14', 'full'), ('tr28', 'none'), ('tr28', 'strat'), ('tr28', 'full'),
         ('auc0_28', 'none'), ('auc0_28', 'strat'), ('auc0_28', 'full'), ('iv', 'none'), ('iv', 'strat')]
late = [('d84', 'none'), ('d84', 'full'), ('cavg_ind', 'none'), ('cavg_ind', 'full')]
inter = [('tr56', 'none'), ('tr56', 'full')]
rows = {k: [] for k in clean + late + inter}
good = []
for s in range(1, n + 1):
    out, truth = S.run(s, verbose=False)
    for k in rows:
        rows[k].append(out[k][1])
    ce = max(out[k][1] for k in clean)
    lt = min(out[k][1] for k in late)
    if ce <= 3.0 and lt >= 9.0:
        good.append((s, round(ce, 1), round(lt, 1), round(truth, 2)))
for k, v in rows.items():
    v = np.array(v)
    print('%-22s median %5.1f  p10 %5.1f  p90 %5.1f  max %5.1f' % (k, np.median(v), np.quantile(v, .1), np.quantile(v, .9), v.max()))
print('good seeds (clean max <= 3, late min >= 9):', len(good), good[:12])
