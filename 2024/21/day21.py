from google.colab import files
uploaded = files.upload()
from itertools import permutations, product

with open("day21.txt") as fin:
    lines = fin.read().strip().split("\n")

numeric_keys = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2)
}
direction_keys = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2)
}

dd = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0)
}

def ways(code, keypad):
    # Number of ways to press code on given keypad
    parts = []
    cur_loc = keypad["A"]

    for c in code:
        # Get to this position
        next_loc = keypad[c]
        di = next_loc[0] - cur_loc[0]
        dj = next_loc[1] - cur_loc[1]

        moves = ""
        if di > 0:
            moves += "v" * di
        elif di < 0:
            moves += "^" * -di
        if dj > 0:
            moves += ">" * dj
        elif dj < 0:
            moves += "<" * -dj
        
        raw_combos = list(set(["".join(x) + "A" for x in permutations(moves)]))
        combos = []
        for combo in raw_combos:
            ci, cj = cur_loc
            good = True
            for c in combo[:-1]:
                di, dj = dd[c]
                ci, cj = ci + di, cj + dj
                if not (ci, cj) in keypad.values():
                    good = False
                    break
            if good:
                combos.append(combo)

        parts.append(combos)
        cur_loc = next_loc
    
    return ["".join(x) for x in product(*parts)]


def shortest3(code):
    ways1 = ways(code, numeric_keys)
    ways2 = []
    for way in ways1:
        ways2.extend(ways(way, direction_keys))
    ways3 = []
    for way in ways2:
        ways3.extend(ways(way, direction_keys))

    return min([len(x) for x in ways3])

ans = 0
for line in lines:
    print(shortest3(line), int(line[:-1]))
    ans += shortest3(line) * int(line[:-1])

print(ans)
import fileinput, functools

n = [ "789", "456", "123", " 0A" ]
d = [ " ^A", "<v>" ]

def path( p, f, t ):
    fx, fy = next( ( x, y ) for y, r in enumerate( p ) for x, c in enumerate( r ) if c == f )
    tx, ty = next( ( x, y ) for y, r in enumerate( p ) for x, c in enumerate( r ) if c == t )
    def g( x, y, s ):
        if ( x, y ) == ( tx, ty ):             yield s + 'A'
        if tx < x and p[ y ][ x - 1 ] != ' ': yield from g( x - 1, y, s + '<' )
        if ty < y and p[ y - 1 ][ x ] != ' ': yield from g( x, y - 1, s + '^' )
        if ty > y and p[ y + 1 ][ x ] != ' ': yield from g( x, y + 1, s + 'v' )
        if tx > x and p[ y ][ x + 1 ] != ' ': yield from g( x + 1, y, s + '>' )
    return min( g( fx, fy, "" ),
                key = lambda p: sum( a != b for a, b in zip( p, p[ 1 : ] ) ) )

@functools.cache
def solve( s, l ):
    if l > 25: return len( s )
    return sum( solve( path( d if l else n, f, t ), l + 1 ) for f, t in zip( 'A' + s, s ) )

print( sum( solve( s.strip(), 0 ) * int( s[ : 3 ] )
            for s in fileinput.input("day21.txt") ) )
