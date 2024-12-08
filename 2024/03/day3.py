import re

def calculate_sum_with_conditions(file_path):
    # Read the corrupted memory from the file
    with open(file_path, 'r') as file:
        corrupted_memory = file.read()
    
    # Regular expression patterns
    mul_pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"  # Match mul(X,Y)
    control_pattern = r"(do\(\)|don't\(\))"  # Match do() or don't()
    
    # Find all mul instructions and control statements
    mul_matches = re.finditer(mul_pattern, corrupted_memory)
    control_matches = re.finditer(control_pattern, corrupted_memory)
    
    # Track whether mul instructions are enabled (starts enabled)
    enabled = True
    total_sum = 0
    control_index = 0
    controls = list(control_matches)
    
    for mul_match in mul_matches:
        # Check if the current mul instruction is affected by any control statement
        while control_index < len(controls) and controls[control_index].start() < mul_match.start():
            control = controls[control_index].group()
            if control == "do()":
                enabled = True
            elif control == "don't()":
                enabled = False
            control_index += 1
        
        # If mul instructions are currently enabled, calculate the result
        if enabled:
            x, y = map(int, mul_match.groups())
            total_sum += x * y
    
    return total_sum

if __name__ == "__main__":
    # Replace 'day3.txt' with your input file name
    file_path = 'day3.txt'
    total = calculate_sum_with_conditions(file_path)
    print(f"Total sum of enabled mul instructions: {total}")
