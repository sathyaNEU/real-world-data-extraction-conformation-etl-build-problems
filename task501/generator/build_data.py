"""Stage 1 of the task501 build: simulate and write the data files, then print the ladder for tuning."""
import os, sys, time
import sim, pack

def run():
    os.makedirs(pack.T, exist_ok=True)
    funds, fx = sim.simulate()
    pack.apply_cancellations(funds)
    fx_get = pack.fx_lookup(fx)
    n_sp = pack.write_spine(funds)
    pack.write_register(funds)
    n_inv = pack.write_investments(funds)
    cells = pack.audited_cells(funds)
    pack.write_audited(funds, cells)
    n_nav, late = pack.write_nav_register(funds, fx_get)
    n_fx = pack.write_fx(fx)
    return funds, fx, cells, dict(spine=n_sp, inv=n_inv, nav=n_nav, fx=n_fx, cells=len(cells))

if __name__ == "__main__":
    t0 = time.time()
    funds, fx, cells, counts = run()
    print("written", counts, round(time.time() - t0, 1), "s")
