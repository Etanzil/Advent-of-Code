import re

ERROR_ADJUSTMENT = 10_000_000_000_000

def parse_input(filename):
    with open(filename, 'r') as f:
        machines = []
        for config in f.read().strip().split("\n\n"):
            ax, ay, bx, by, prize_x, prize_y = map(int, re.findall(r'\d+', config))
            machines.append(((ax, ay), (bx, by), (prize_x, prize_y)))
        return machines

def calculate_min_tokens(machine, error=False):
    (ax, ay), (bx, by), (prize_x, prize_y) = machine

    # Apply error adjustment if needed
    if error:
        prize_x += ERROR_ADJUSTMENT
        prize_y += ERROR_ADJUSTMENT

    # Calculate presses for buttons A and B
    a = (prize_x * by - prize_y * bx) // (ax * by - ay * bx)
    b = (prize_x - ax * a) // bx

    # Validate the solution
    if ax * a + bx * b != prize_x or ay * a + by * b != prize_y:
        return 0  # No valid solution for this machine

    # Return the total token cost
    return 3 * a + b

def solve_claw_machines(filename):
    machines = parse_input(filename)
    total_tokens = sum(calculate_min_tokens(machine) for machine in machines)
    total_error_tokens = sum(calculate_min_tokens(machine, error=True) for machine in machines)
    return total_tokens, total_error_tokens

if __name__ == "__main__":
    filename = "day13.txt"  # Replace with your input file
    prizes, adjusted_prizes = solve_claw_machines(filename)
    print(f"Fewest tokens required: {prizes}")
    print(f"Fewest tokens required (adjusted): {adjusted_prizes}")
