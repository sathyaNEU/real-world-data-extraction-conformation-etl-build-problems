"""Run the assertion suite against an existing target without rebuilding the pack (rebuilds the world in memory)."""
import sys
from pathlib import Path
from reportlab import rl_config
rl_config.invariant = 1
import assemble, cast, asserts
from world import Register
T = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "target"
reg = Register()
c = cast.Cast(reg).run()
A = assemble.Assembly(reg, c).build()
import extracts
extracts.ledger(reg, A)
asserts.run(T, reg, c, A, None)
