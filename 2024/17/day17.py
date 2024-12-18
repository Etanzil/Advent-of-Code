from z3 import *

# Initialize optimizer
opt = Optimize()

# Define s, a, b, and c as BitVecs
s = BitVec('s', 64)
a = s  # a is initialized to s
b = BitVec('b', 64)  # b is a BitVec variable
c = BitVec('c', 64)  # c is also a BitVec variable

# Integer 5 as a BitVec
five = BitVecVal(5, 64)  # 5 as a 64-bit BitVec

# Expected output sequence
expected_output = [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0]

# Loop through the expected output sequence
for x in expected_output:
    # Perform operations as described
    b = URem(a, 8)           # b = a % 8
    b = Xor(b, five)         # b = b ^ 5 (5 is now a BitVec)
    c = UDiv(a, (1 << b))    # c = a / (1 << b)
    b = Xor(b, c)            # b = b ^ c
    b = Xor(b, 6)            # b = b ^ 6
    a = UDiv(a, (1 << 3))    # a = a / (1 << 3)
    
    # Assert that the value of b % 8 matches the expected output
    opt.add(URem(b, 8) == x)

# Add the constraint that a must be zero at the end
opt.add(a == 0)

# Minimize the initial value of s
opt.minimize(s)

# Check if a solution exists
if opt.check() == sat:
    print("The smallest initial value for s is:", opt.model().eval(s))
else:
    print("No valid solution found.")
