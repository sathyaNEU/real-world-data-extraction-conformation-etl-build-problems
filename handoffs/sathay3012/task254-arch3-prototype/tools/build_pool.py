import json, os, re, subprocess, sys, shutil
repo = sys.argv[1]; out = sys.argv[2]; me = sys.argv[3]  # me: own branch to skip
CARDS = ".claude/skills/fingerprint/cards"
def git(*a):
    return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True).stdout
if os.path.isdir(out): shutil.rmtree(out)
os.makedirs(out)
# main's cards
for line in git("ls-tree", "--name-only", "origin/main", CARDS + "/").split():
    if line.endswith(".json"):
        open(os.path.join(out, os.path.basename(line)), "w").write(git("show", "origin/main:" + line))
best = {}
branches = [b.strip() for b in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").split("\n") if b.strip()]
for b in branches:
    if b in ("origin/main", "origin/HEAD", "origin") or b == "origin/" + me: continue
    nums = set(re.findall(r"task(\d+)", b)) | set(re.findall(r"cards-(\d+)", b))
    for n in nums:
        path = "%s/task%s.json" % (CARDS, n)
        body = git("show", "%s:%s" % (b, path))
        if not body.strip(): continue
        ts = git("log", "-1", "--format=%ct", b, "--", path).strip()
        ts = int(ts) if ts else 0
        try: card = json.loads(body)
        except Exception: continue
        key = "task" + n
        if key not in best or ts > best[key][0]:
            best[key] = (ts, b, body, card.get("architecture"))
for key, (ts, b, body, arch) in sorted(best.items()):
    mainbody = git("show", "origin/main:%s/%s.json" % (CARDS, key))
    mts = git("log", "-1", "--format=%ct", "origin/main", "--", "%s/%s.json" % (CARDS, key)).strip()
    mts = int(mts) if mts else 0
    if mainbody.strip() and mts >= ts:
        print("main newer or equal", key); continue
    open(os.path.join(out, key + ".json"), "w").write(body)
    print("in-flight", key, arch, "from", b)
print("cards:", len([f for f in os.listdir(out) if f.endswith('.json')]))
