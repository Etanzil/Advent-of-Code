from collections import defaultdict
data = open("day23.txt").read()

g = defaultdict(set)
for a, b in [line.split("-") for line in data.split("\n")]:
    g[a].add(b)
    g[b].add(a)

p1 = set(",".join(sorted([c, a, b])) for c in g for a in g[c] for b in g[c]
                                     if c.startswith("t") and b in g[a])
print("Part 1:", len(p1))

def find_clique(target_size=13):
    for c1 in g:
        for c2 in g[c1]:
            m = set.intersection(*({a} | g[a] for a in g[c1] if a != c2))
            if len(m) == target_size: 
                return sorted(m)
print("Part 2:", ",".join(find_clique()))
