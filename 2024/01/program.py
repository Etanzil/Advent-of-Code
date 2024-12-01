i = open("input.txt").read().strip().split("\n")


part1 = part2 = 0
l1 = []
l2 = []
for l in i:
    l1 += [ int(l.split("   ")[0]) ]
    l2 += [ int(l.split("   ")[1]) ]

l1.sort()
l2.sort()
for ix in range(len(l1)):
    part1 += abs(l1[ix] - l2[ix])
    part2 += (l1[ix] * sum(k == l1[ix] for k in l2)) 


print(part1)

print(part2)
