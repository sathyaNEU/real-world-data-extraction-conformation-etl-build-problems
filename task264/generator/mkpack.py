import sys, time
from world import build_all
from pack import write_pack
t = time.time()
A = build_all()
n = write_pack(A, sys.argv[1])
print(n, round(time.time() - t, 1), "s")
